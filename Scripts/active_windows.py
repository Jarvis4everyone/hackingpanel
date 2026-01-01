"""
Active Windows Monitor
Lists all visible windows with their titles and process info
"""
import os
import sys
import ctypes
from ctypes import wintypes
from datetime import datetime

# Windows API functions
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

def get_window_list():
    """Get list of all visible windows."""
    windows = []
    
    EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    
    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            # Get window title
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                title = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, title, length + 1)
                
                if title.value.strip():
                    # Get process ID
                    pid = wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    
                    # Get process name
                    process_name = "Unknown"
                    h_process = kernel32.OpenProcess(0x0400 | 0x0010, False, pid.value)
                    if h_process:
                        try:
                            name_buffer = ctypes.create_unicode_buffer(260)
                            psapi.GetModuleBaseNameW(h_process, None, name_buffer, 260)
                            process_name = name_buffer.value
                        except:
                            pass
                        kernel32.CloseHandle(h_process)
                    
                    # Get window position and size
                    rect = wintypes.RECT()
                    user32.GetWindowRect(hwnd, ctypes.byref(rect))
                    
                    windows.append({
                        'hwnd': hwnd,
                        'title': title.value,
                        'pid': pid.value,
                        'process': process_name,
                        'x': rect.left,
                        'y': rect.top,
                        'width': rect.right - rect.left,
                        'height': rect.bottom - rect.top
                    })
        return True
    
    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return windows


def get_foreground_window():
    """Get the currently active window."""
    hwnd = user32.GetForegroundWindow()
    
    length = user32.GetWindowTextLengthW(hwnd)
    title = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, title, length + 1)
    
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    
    process_name = "Unknown"
    h_process = kernel32.OpenProcess(0x0400 | 0x0010, False, pid.value)
    if h_process:
        try:
            name_buffer = ctypes.create_unicode_buffer(260)
            psapi.GetModuleBaseNameW(h_process, None, name_buffer, 260)
            process_name = name_buffer.value
        except:
            pass
        kernel32.CloseHandle(h_process)
    
    return {
        'hwnd': hwnd,
        'title': title.value,
        'pid': pid.value,
        'process': process_name
    }


def main():
    print("=" * 70)
    print("ACTIVE WINDOWS MONITOR")
    print("=" * 70)
    print(f"Captured at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get foreground window
    print("\n[*] Currently Active Window:")
    fg = get_foreground_window()
    print(f"    Title: {fg['title']}")
    print(f"    Process: {fg['process']} (PID: {fg['pid']})")
    
    # Get all windows
    print("\n[*] All Visible Windows:")
    print("-" * 70)
    
    windows = get_window_list()
    
    # Sort by process name
    windows.sort(key=lambda x: x['process'].lower())
    
    # Group by process
    processes = {}
    for win in windows:
        proc = win['process']
        if proc not in processes:
            processes[proc] = []
        processes[proc].append(win)
    
    for i, (proc, wins) in enumerate(sorted(processes.items()), 1):
        print(f"\n{i}. {proc} ({len(wins)} window(s))")
        for win in wins:
            title = win['title'][:50] + "..." if len(win['title']) > 50 else win['title']
            print(f"   - {title}")
            print(f"     PID: {win['pid']} | Position: ({win['x']}, {win['y']}) | Size: {win['width']}x{win['height']}")
    
    print("\n" + "-" * 70)
    print(f"Total: {len(windows)} visible windows from {len(processes)} processes")
    
    # Summary by process
    print("\n[*] Summary by Process:")
    for proc, wins in sorted(processes.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"    {proc}: {len(wins)} window(s)")


if __name__ == '__main__':
    if sys.platform != 'win32':
        print("This script only works on Windows")
        sys.exit(1)
    main()

