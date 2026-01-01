# -*- coding: utf-8 -*-
"""
Taskbar Hide/Show Toggle
Hides or shows the Windows taskbar
"""
import ctypes
import os

# Get action from environment (hide/show/toggle)
ACTION = os.environ.get("TASKBAR_ACTION", "toggle").lower()

print("=" * 50)
print("   TASKBAR HIDE/SHOW")
print("=" * 50)
print(f"   Action: {ACTION}")
print("=" * 50)

user32 = ctypes.windll.user32

# Constants
SW_HIDE = 0
SW_SHOW = 5
ABM_SETSTATE = 0x0000000A
ABS_AUTOHIDE = 0x01
ABS_ALWAYSONTOP = 0x02

def find_taskbar():
    """Find the taskbar window."""
    return user32.FindWindowW("Shell_TrayWnd", None)

def is_taskbar_visible():
    """Check if taskbar is visible."""
    taskbar = find_taskbar()
    if taskbar:
        return user32.IsWindowVisible(taskbar)
    return True

def hide_taskbar():
    """Hide the taskbar."""
    taskbar = find_taskbar()
    if taskbar:
        user32.ShowWindow(taskbar, SW_HIDE)
        print("[OK] Taskbar hidden!")
        return True
    return False

def show_taskbar():
    """Show the taskbar."""
    taskbar = find_taskbar()
    if taskbar:
        user32.ShowWindow(taskbar, SW_SHOW)
        print("[OK] Taskbar shown!")
        return True
    return False

def toggle_taskbar():
    """Toggle taskbar visibility."""
    if is_taskbar_visible():
        hide_taskbar()
    else:
        show_taskbar()

try:
    taskbar = find_taskbar()
    
    if not taskbar:
        print("[!] Could not find taskbar window")
    else:
        current_state = "visible" if is_taskbar_visible() else "hidden"
        print(f"[*] Current state: {current_state}")
        
        if ACTION == "hide":
            hide_taskbar()
        elif ACTION == "show":
            show_taskbar()
        else:  # toggle
            toggle_taskbar()
        
        new_state = "visible" if is_taskbar_visible() else "hidden"
        print(f"[*] New state: {new_state}")

except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 50)
print("Tip: Run again to toggle back, or set TASKBAR_ACTION=show")
print("=" * 50)

