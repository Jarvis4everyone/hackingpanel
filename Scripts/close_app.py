# -*- coding: utf-8 -*-
"""
Close Application
Closes an application by name using appopener or process name
"""
import os
import subprocess
import sys
import time

# Get app name from environment variable (set by server)
APP_NAME = os.environ.get("APP_NAME", "")

print("=" * 60)
print("   CLOSE APPLICATION")
print("=" * 60)

def close_by_appopener(app_name):
    """Try to close using AppOpener library."""
    try:
        # Try the working import pattern: from AppOpener import close
        try:
            from AppOpener import close
            print(f"[*] AppOpener imported successfully")
        except ImportError:
            # If not found, install and try again
            print("[*] AppOpener not found, installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "appopener", "-q"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            from AppOpener import close
            print(f"[*] AppOpener installed and imported")
        
        print(f"[*] Attempting to close using AppOpener: {app_name}")
        # Use the close function directly (matches working example)
        close(app_name)
        time.sleep(1.0)  # Give it time to close
        
        # Check if still running
        if not is_app_running(app_name):
            print(f"[OK] Successfully closed using AppOpener: {app_name}")
            return True
        else:
            print(f"[!] AppOpener close command executed, but app may still be running")
    except Exception as e:
        print(f"[!] AppOpener method failed: {e}")
        import traceback
        traceback.print_exc()
    
    return False

def is_app_running(app_name):
    """Check if application is still running."""
    try:
        app_lower = app_name.lower().strip()
        # Remove .exe if present
        if app_lower.endswith('.exe'):
            app_lower = app_lower[:-4]
        
        # Try tasklist first
        result = subprocess.run(
            ['tasklist', '/FI', f'IMAGENAME eq {app_lower}.exe'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if app_lower in result.stdout.lower():
            return True
        
        # Also try without .exe extension
        result2 = subprocess.run(
            ['tasklist'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if app_lower in result2.stdout.lower():
            return True
    except:
        pass
    
    # Try with PowerShell (more flexible)
    try:
        ps_script = f'Get-Process -Name "*{app_name}*" -ErrorAction SilentlyContinue | Select-Object -First 1'
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=5
        )
        return bool(result.stdout.strip())
    except:
        return False

def close_by_process_name(app_name):
    """Close application by process name."""
    try:
        app_lower = app_name.lower()
        
        # Try taskkill with exact name
        print(f"[*] Attempting to close process: {app_name}.exe")
        result = subprocess.run(
            ['taskkill', '/F', '/IM', f'{app_name}.exe'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print(f"[OK] Successfully closed: {app_name}")
            return True
        
        # Try with PowerShell (more flexible)
        print(f"[*] Attempting to close using PowerShell...")
        ps_script = f'''
        $processes = Get-Process | Where-Object {{ $_.ProcessName -like "*{app_name}*" }}
        if ($processes) {{
            $processes | Stop-Process -Force
            Write-Output "Closed"
        }} else {{
            Write-Output "NotFound"
        }}
        '''
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if "Closed" in result.stdout:
            print(f"[OK] Successfully closed: {app_name}")
            return True
            
    except Exception as e:
        print(f"[!] Process kill method failed: {e}")
    
    return False

def main():
    if not APP_NAME:
        print("\n[!] ERROR: No application name provided!")
        print("    Set APP_NAME environment variable.")
        return
    
    print(f"\n[*] Target application: {APP_NAME}")
    
    # Check if app is running first
    if not is_app_running(APP_NAME):
        print(f"[OK] Application '{APP_NAME}' is not running (already closed)")
        return
    
    print(f"[*] Application '{APP_NAME}' is currently running")
    
    # Method 1: Try appopener (most reliable)
    print("\n[*] Method 1: Trying appopener...")
    if close_by_appopener(APP_NAME):
        # Double check
        time.sleep(0.5)
        if not is_app_running(APP_NAME):
            print(f"[OK] Confirmed: {APP_NAME} has been closed")
            return
        else:
            print(f"[!] appopener reported success but app still appears running, trying fallback...")
    
    # Method 2: Try process name
    print("\n[*] Method 2: Trying process termination...")
    if close_by_process_name(APP_NAME):
        # Double check
        time.sleep(0.5)
        if not is_app_running(APP_NAME):
            print(f"[OK] Confirmed: {APP_NAME} has been closed")
            return
    
    print(f"\n[ERROR] Could not close: {APP_NAME}")
    print("\n[*] Tips:")
    print("    - Make sure the application name is correct")
    print("    - The app might require admin privileges to close")
    print("    - Some system apps cannot be closed")
    print("    - Try using the exact process name (e.g., 'chrome' not 'Google Chrome')")

if __name__ == '__main__':
    main()

