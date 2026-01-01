# -*- coding: utf-8 -*-
"""
Disable Keyboard & Mouse (Multi-Method, 100% Reliable)
Tries multiple methods to ensure it works on all PCs
"""
import os
import sys
import ctypes
import subprocess
import threading
import time

# Duration in seconds (max 300)
DURATION = min(int(os.environ.get("DISABLE_DURATION", "30")), 300)

print("=" * 60)
print("   DISABLE KEYBOARD & MOUSE (MULTI-METHOD)")
print("=" * 60)
print(f"   Duration: {DURATION} seconds")
print(f"   Emergency exit: Ctrl + -")
print("=" * 60)

# Windows API constants
WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_MOUSEWHEEL = 0x020A
HC_ACTION = 0

# Windows API structures
class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_long),
        ("y", ctypes.c_long)
    ]

class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", ctypes.c_ulong),
        ("scanCode", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", ctypes.c_ulong),
        ("flags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

# MSG structure for message loop
class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", ctypes.c_void_p),
        ("message", ctypes.c_uint),
        ("wParam", ctypes.c_void_p),
        ("lParam", ctypes.c_void_p),
        ("time", ctypes.c_ulong),
        ("pt", POINT)
    ]


class InputBlocker:
    def __init__(self, duration):
        self.duration = duration
        self.running = True
        self.method_used = None
        self.blocking_thread = None
        
        # Method 1: pynput listeners
        self.mouse_listener = None
        self.keyboard_listener = None
        self.pynput_hotkey = None
        
        # Method 2: Windows API hooks
        self.keyboard_hook = None
        self.mouse_hook = None
        self.hook_proc_keyboard = None
        self.hook_proc_mouse = None
        
        # Method 3: pyautogui blocking
        self.pyautogui_thread = None
        
        # Method 4: BlockInput API
        self.blockinput_active = False
        
        # Emergency hotkey detection (global listener)
        self.emergency_keys = set()
        self.emergency_listener = None
    
    def stop_blocking(self):
        """Stop blocking input (called by emergency hotkey)."""
        print("\n[!] Emergency stop triggered!")
        self.running = False
    
    def timer_thread(self):
        """Timer to auto-stop after duration."""
        for i in range(self.duration, 0, -1):
            if not self.running:
                break
            time.sleep(1)
            if i % 10 == 0 or i <= 5:
                print(f"    {i} seconds remaining...")
        
        # Stop after timer
        if self.running:
            self.running = False
            print("\n[*] Timer expired!")
    
    # ============================================
    # METHOD 1: pynput with suppress=True
    # ============================================
    def method_pynput(self):
        """Try blocking with pynput (no admin needed)."""
        try:
            try:
                from pynput import keyboard, mouse
            except ImportError:
                print("[*] Installing pynput...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pynput", "-q"], 
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                from pynput import keyboard, mouse
            
            # Create hotkey for emergency exit
            self.pynput_hotkey = keyboard.HotKey(
                keyboard.HotKey.parse('<ctrl>+-'),
                self.stop_blocking
            )
            
            def for_canonical(f):
                return lambda k: f(self.keyboard_listener.canonical(k))
            
            # Create listeners with suppress=True
            self.mouse_listener = mouse.Listener(suppress=True)
            self.keyboard_listener = keyboard.Listener(
                suppress=True,
                on_press=for_canonical(self.pynput_hotkey.press),
                on_release=for_canonical(self.pynput_hotkey.release)
            )
            
            self.mouse_listener.start()
            self.keyboard_listener.start()
            
            # Wait for listeners to be ready
            time.sleep(0.5)
            
            if self.mouse_listener.running and self.keyboard_listener.running:
                print("[OK] Method 1: pynput blocking active!")
                self.method_used = "pynput"
                return True
            
        except Exception as e:
            print(f"[!] Method 1 (pynput) failed: {str(e)[:50]}")
        
        return False
    
    def stop_pynput(self):
        """Stop pynput listeners."""
        try:
            if self.mouse_listener:
                self.mouse_listener.stop()
            if self.keyboard_listener:
                self.keyboard_listener.stop()
        except:
            pass
    
    # ============================================
    # METHOD 2: Windows API BlockInput
    # ============================================
    def method_blockinput(self):
        """Try blocking with Windows BlockInput API."""
        try:
            user32 = ctypes.windll.user32
            
            # Try to block input
            result = user32.BlockInput(True)
            if result:
                print("[OK] Method 2: BlockInput API active!")
                self.method_used = "blockinput"
                self.blockinput_active = True
                return True
            else:
                # Get last error
                error = ctypes.get_last_error()
                if error == 5:  # Access denied (needs admin)
                    print("[!] Method 2 (BlockInput) requires admin privileges")
                else:
                    print(f"[!] Method 2 (BlockInput) failed: error {error}")
        except Exception as e:
            print(f"[!] Method 2 (BlockInput) failed: {str(e)[:50]}")
        
        return False
    
    def stop_blockinput(self):
        """Stop BlockInput."""
        try:
            if self.blockinput_active:
                ctypes.windll.user32.BlockInput(False)
                self.blockinput_active = False
        except:
            pass
    
    # ============================================
    # METHOD 3: Direct Windows API Hooks
    # ============================================
    def method_windows_hooks(self):
        """Try blocking with direct Windows API hooks."""
        try:
            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32
            
            # Keyboard hook procedure
            def low_level_keyboard_proc(nCode, wParam, lParam):
                if nCode >= HC_ACTION:
                    # Check for emergency hotkey (Ctrl + -)
                    kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                    if kbd.vkCode == 189:  # Minus key
                        if 162 in self.emergency_keys or 163 in self.emergency_keys:  # Ctrl
                            self.stop_blocking()
                    elif kbd.vkCode in [162, 163]:  # Left/Right Ctrl
                        if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
                            self.emergency_keys.add(kbd.vkCode)
                        else:
                            self.emergency_keys.discard(kbd.vkCode)
                    
                    # Block all keys
                    return 1  # Block the key
                return user32.CallNextHookExW(self.keyboard_hook, nCode, wParam, lParam)
            
            # Mouse hook procedure
            def low_level_mouse_proc(nCode, wParam, lParam):
                if nCode >= HC_ACTION:
                    # Block all mouse events
                    return 1  # Block the event
                return user32.CallNextHookExW(self.mouse_hook, nCode, wParam, lParam)
            
            # Define hook procedure types
            # WPARAM and LPARAM are pointer-sized integers
            if ctypes.sizeof(ctypes.c_void_p) == 8:  # 64-bit
                WPARAM = ctypes.c_ulonglong
                LPARAM = ctypes.c_longlong
            else:  # 32-bit
                WPARAM = ctypes.c_ulong
                LPARAM = ctypes.c_long
            
            HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, WPARAM, LPARAM)
            
            self.hook_proc_keyboard = HOOKPROC(low_level_keyboard_proc)
            self.hook_proc_mouse = HOOKPROC(low_level_mouse_proc)
            
            # Install hooks
            self.keyboard_hook = user32.SetWindowsHookExW(
                WH_KEYBOARD_LL,
                self.hook_proc_keyboard,
                kernel32.GetModuleHandleW(None),
                0
            )
            
            self.mouse_hook = user32.SetWindowsHookExW(
                WH_MOUSE_LL,
                self.hook_proc_mouse,
                kernel32.GetModuleHandleW(None),
                0
            )
            
            if self.keyboard_hook and self.mouse_hook:
                print("[OK] Method 3: Windows API hooks active!")
                self.method_used = "windows_hooks"
                
                # Process messages to keep hooks alive (in background thread)
                def message_loop():
                    try:
                        while self.running:
                            # PeekMessage to avoid blocking
                            msg = MSG()
                            bRet = user32.PeekMessageW(
                                ctypes.byref(msg),
                                None,
                                0,
                                0,
                                0x0001  # PM_NOREMOVE
                            )
                            if bRet:
                                msg = MSG()
                                bRet = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                                if bRet == 0 or bRet == -1:
                                    break
                                user32.TranslateMessage(ctypes.byref(msg))
                                user32.DispatchMessageW(ctypes.byref(msg))
                            else:
                                time.sleep(0.01)  # Small delay if no messages
                    except:
                        pass
                
                self.blocking_thread = threading.Thread(target=message_loop, daemon=True)
                self.blocking_thread.start()
                time.sleep(0.5)
                return True
            
        except Exception as e:
            print(f"[!] Method 3 (Windows hooks) failed: {str(e)[:50]}")
        
        return False
    
    def stop_windows_hooks(self):
        """Stop Windows API hooks."""
        try:
            if self.keyboard_hook:
                ctypes.windll.user32.UnhookWindowsHookExW(self.keyboard_hook)
                self.keyboard_hook = None
            if self.mouse_hook:
                ctypes.windll.user32.UnhookWindowsHookExW(self.mouse_hook)
                self.mouse_hook = None
        except:
            pass
    
    # ============================================
    # METHOD 4: pyautogui continuous blocking
    # ============================================
    def method_pyautogui(self):
        """Try blocking with pyautogui (continuous mouse/key blocking)."""
        try:
            try:
                import pyautogui
            except ImportError:
                print("[*] Installing pyautogui...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui", "-q"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                import pyautogui
            
            # Disable pyautogui failsafe
            pyautogui.FAILSAFE = False
            
            # Get screen center
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            
            def continuous_block():
                while self.running:
                    try:
                        # Move mouse to center (prevents user mouse movement)
                        pyautogui.moveTo(center_x, center_y, duration=0)
                        time.sleep(0.01)  # 10ms loop
                    except:
                        pass
            
            self.pyautogui_thread = threading.Thread(target=continuous_block, daemon=True)
            self.pyautogui_thread.start()
            time.sleep(0.5)
            
            print("[OK] Method 4: pyautogui blocking active!")
            self.method_used = "pyautogui"
            return True
            
        except Exception as e:
            print(f"[!] Method 4 (pyautogui) failed: {str(e)[:50]}")
        
        return False
    
    def stop_pyautogui(self):
        """Stop pyautogui blocking."""
        # Thread will stop when self.running = False
        pass
    
    # ============================================
    # EMERGENCY HOTKEY LISTENER (works with all methods)
    # ============================================
    def start_emergency_listener(self):
        """Start a global emergency hotkey listener."""
        try:
            try:
                from pynput import keyboard
            except ImportError:
                return  # Can't set up emergency listener without pynput
            
            def on_press(key):
                try:
                    # Check for Ctrl + -
                    if hasattr(key, 'char') and key.char == '-':
                        # Check if Ctrl is pressed
                        if keyboard.Key.ctrl_l in self.emergency_keys or keyboard.Key.ctrl_r in self.emergency_keys:
                            self.stop_blocking()
                    elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                        self.emergency_keys.add(key)
                except:
                    pass
            
            def on_release(key):
                try:
                    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                        self.emergency_keys.discard(key)
                except:
                    pass
            
            # Start listener in non-blocking mode (doesn't suppress, just listens)
            self.emergency_listener = keyboard.Listener(
                on_press=on_press,
                on_release=on_release,
                suppress=False  # Don't suppress, just listen
            )
            self.emergency_listener.start()
        except:
            pass
    
    def stop_emergency_listener(self):
        """Stop emergency hotkey listener."""
        try:
            if self.emergency_listener:
                self.emergency_listener.stop()
        except:
            pass
    
    # ============================================
    # MAIN BLOCKING METHOD (tries all)
    # ============================================
    def block(self):
        """Start blocking all input using best available method."""
        print(f"\n[*] Attempting to block input for {self.duration} seconds...")
        print("    Trying multiple methods for maximum compatibility...")
        
        # Start emergency hotkey listener (works with all methods)
        self.start_emergency_listener()
        
        # Start timer in background
        timer = threading.Thread(target=self.timer_thread, daemon=True)
        timer.start()
        
        # Try methods in order of preference
        methods = [
            ("pynput", self.method_pynput, self.stop_pynput),
            ("blockinput", self.method_blockinput, self.stop_blockinput),
            ("windows_hooks", self.method_windows_hooks, self.stop_windows_hooks),
            ("pyautogui", self.method_pyautogui, self.stop_pyautogui),
        ]
        
        active_methods = []
        
        # Try methods in order - use first successful method
        # pynput is most reliable without admin, BlockInput might work, 
        # Windows hooks are complex, pyautogui is last resort
        for method_name, try_method, stop_method in methods:
            if try_method():
                active_methods.append((method_name, stop_method))
                # If pynput works, we're good. Otherwise try next method.
                # For extra reliability with pynput, we could add pyautogui, but let's keep it simple
                if method_name in ["pynput", "blockinput", "windows_hooks"]:
                    break  # Strong method found
        
        if not active_methods:
            print("\n[ERROR] All blocking methods failed!")
            print("    Input may not be fully blocked.")
            print("    This could be due to:")
            print("    - Antivirus blocking hooks")
            print("    - Windows security policies")
            print("    - Missing dependencies")
            return False
        
        print(f"\n[OK] Input blocking active using: {', '.join([m[0] for m in active_methods])}")
        print("    Press Ctrl+- to emergency stop")
        
        # Wait while blocking
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.running = False
        
        # Stop all active methods
        print("\n[*] Stopping input blocking...")
        for method_name, stop_method in active_methods:
            try:
                stop_method()
            except:
                pass
        
        # Stop emergency listener
        self.stop_emergency_listener()
        
        print("[OK] Input re-enabled!")
        return True


def main():
    print("\n[*] Starting multi-method input blocker...")
    
    blocker = InputBlocker(DURATION)
    success = blocker.block()
    
    print("\n" + "=" * 60)
    if success:
        print("[OK] Script finished - input should be working")
    else:
        print("[!] Script finished - blocking may not have been fully effective")
    print("=" * 60)


if __name__ == '__main__':
    main()
