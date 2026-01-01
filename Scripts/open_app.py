# -*- coding: utf-8 -*-
"""
Open Application
Opens an application by name using appopener (no path needed)
"""
import os
import subprocess
import sys
import time

# Get app name/path from environment variable (set by server)
APP_NAME = os.environ.get("APP_NAME", "")
APP_ARGS = os.environ.get("APP_ARGS", "")  # Optional arguments

# Common application mappings
APP_SHORTCUTS = {
    # Browsers
    'chrome': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'firefox': r'C:\Program Files\Mozilla Firefox\firefox.exe',
    'edge': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    'brave': r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe',
    'opera': r'C:\Program Files\Opera\opera.exe',
    
    # Microsoft Office
    'word': r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE',
    'excel': r'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE',
    'powerpoint': r'C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE',
    'outlook': r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE',
    
    # Development
    'vscode': r'C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe',
    'notepad++': r'C:\Program Files\Notepad++\notepad++.exe',
    'git': r'C:\Program Files\Git\git-bash.exe',
    
    # Media
    'vlc': r'C:\Program Files\VideoLAN\VLC\vlc.exe',
    'spotify': r'C:\Users\%USERNAME%\AppData\Roaming\Spotify\Spotify.exe',
    
    # Utilities
    'notepad': 'notepad.exe',
    'calc': 'calc.exe',
    'calculator': 'calc.exe',
    'paint': 'mspaint.exe',
    'cmd': 'cmd.exe',
    'powershell': 'powershell.exe',
    'terminal': 'wt.exe',
    'explorer': 'explorer.exe',
    'taskmgr': 'taskmgr.exe',
    'taskmanager': 'taskmgr.exe',
    'control': 'control.exe',
    'settings': 'ms-settings:',
    'snipping': 'snippingtool.exe',
    'snip': 'snippingtool.exe',
    
    # Communication
    'discord': r'C:\Users\%USERNAME%\AppData\Local\Discord\Update.exe --processStart Discord.exe',
    'slack': r'C:\Users\%USERNAME%\AppData\Local\slack\slack.exe',
    'zoom': r'C:\Users\%USERNAME%\AppData\Roaming\Zoom\bin\Zoom.exe',
    'teams': r'C:\Users\%USERNAME%\AppData\Local\Microsoft\Teams\current\Teams.exe',
    'telegram': r'C:\Users\%USERNAME%\AppData\Roaming\Telegram Desktop\Telegram.exe',
    'whatsapp': 'shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App',
    
    # Games
    'steam': r'C:\Program Files (x86)\Steam\steam.exe',
    'epicgames': r'C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe',
}


def find_app_in_start_menu(app_name):
    """Search for app in Start Menu."""
    start_paths = [
        os.path.expandvars(r'%ProgramData%\Microsoft\Windows\Start Menu\Programs'),
        os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
    ]
    
    app_lower = app_name.lower()
    
    for start_path in start_paths:
        if os.path.exists(start_path):
            for root, dirs, files in os.walk(start_path):
                for file in files:
                    if file.endswith('.lnk'):
                        if app_lower in file.lower():
                            return os.path.join(root, file)
    
    return None


def find_app_in_path(app_name):
    """Search for app in system PATH."""
    try:
        # Try using 'where' command
        result = subprocess.run(
            ['where', app_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split('\n')[0]
    except:
        pass
    
    return None


def open_store_app(app_name):
    """Try to open a Microsoft Store app."""
    try:
        # Get list of store apps
        result = subprocess.run(
            ['powershell', '-Command', 
             f'Get-AppxPackage | Where-Object {{ $_.Name -like "*{app_name}*" }} | Select-Object -First 1 -ExpandProperty PackageFamilyName'],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout.strip():
            package_family = result.stdout.strip()
            # Open the store app
            subprocess.Popen(f'explorer.exe shell:AppsFolder\\{package_family}!App', shell=True)
            return True
    except:
        pass
    
    return False


def open_application(app_name, args=""):
    """Try to open the application using various methods."""
    app_lower = app_name.lower().strip()
    
    print(f"[*] Attempting to open: {app_name}")
    if args:
        print(f"[*] Arguments: {args}")
    
    # Method 1: Try AppOpener (most reliable, no path needed)
    try:
        try:
            from AppOpener import open as appopener_open
            print(f"[*] AppOpener imported successfully")
        except ImportError:
            # If not found, install and try again
            print("[*] AppOpener not found, installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "appopener", "-q"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            from AppOpener import open as appopener_open
            print(f"[*] AppOpener installed and imported")
        
        print(f"[*] Attempting to open using AppOpener: {app_name}")
        # Use the open function directly (matches working example)
        appopener_open(app_name)
        time.sleep(0.5)  # Give it time to open
        print(f"[OK] Successfully opened: {app_name}")
        return True
    except Exception as e:
        print(f"[!] AppOpener method failed: {e}")
        import traceback
        traceback.print_exc()
        print(f"[*] Trying fallback methods...")
    
    # Method 2: Check shortcuts dictionary
    if app_lower in APP_SHORTCUTS:
        path = os.path.expandvars(APP_SHORTCUTS[app_lower])
        
        # Handle special cases (like ms-settings: or shell:)
        if path.startswith('ms-settings:') or path.startswith('shell:'):
            print(f"[*] Opening via shell: {path}")
            os.system(f'start "" "{path}"')
            return True
        
        if os.path.exists(path.split()[0] if ' ' in path else path):
            print(f"[*] Found in shortcuts: {path}")
            try:
                if args:
                    subprocess.Popen(f'"{path}" {args}', shell=True)
                else:
                    subprocess.Popen(path, shell=True)
                return True
            except Exception as e:
                print(f"    Error: {e}")
    
    # Method 2: Check if it's a direct path
    if os.path.exists(app_name):
        print(f"[*] Opening direct path: {app_name}")
        try:
            os.startfile(app_name)
            return True
        except Exception as e:
            print(f"    Error: {e}")
    
    # Method 3: Search in Start Menu
    print(f"[*] Searching in Start Menu...")
    shortcut = find_app_in_start_menu(app_name)
    if shortcut:
        print(f"[*] Found shortcut: {shortcut}")
        try:
            os.startfile(shortcut)
            return True
        except Exception as e:
            print(f"    Error: {e}")
    
    # Method 4: Search in PATH
    print(f"[*] Searching in PATH...")
    path_app = find_app_in_path(app_name)
    if path_app:
        print(f"[*] Found in PATH: {path_app}")
        try:
            subprocess.Popen(path_app, shell=True)
            return True
        except Exception as e:
            print(f"    Error: {e}")
    
    # Method 5: Try as Windows Store app
    print(f"[*] Trying as Store app...")
    if open_store_app(app_name):
        return True
    
    # Method 6: Try direct execution (maybe it's in PATH)
    print(f"[*] Trying direct execution...")
    try:
        subprocess.Popen(app_name, shell=True)
        return True
    except:
        pass
    
    # Method 7: Try with 'start' command
    print(f"[*] Trying with 'start' command...")
    try:
        os.system(f'start "" "{app_name}"')
        return True
    except:
        pass
    
    return False


def main():
    print("=" * 60)
    print("   OPEN APPLICATION")
    print("=" * 60)
    
    if not APP_NAME:
        print("\n[!] ERROR: No application name provided!")
        print("    Set APP_NAME environment variable.")
        print("\n[*] Available shortcuts:")
        for name in sorted(APP_SHORTCUTS.keys()):
            print(f"    - {name}")
        return
    
    print(f"\n[*] Target application: {APP_NAME}")
    
    if open_application(APP_NAME, APP_ARGS):
        print(f"\n[OK] Successfully opened: {APP_NAME}")
    else:
        print(f"\n[ERROR] Could not open: {APP_NAME}")
        print("\n[*] Tips:")
        print("    - Try the exact application name")
        print("    - Use the full path to the .exe file")
        print("    - Check if the app is installed")
        print("\n[*] Available shortcuts:")
        for name in sorted(APP_SHORTCUTS.keys())[:20]:
            print(f"    - {name}")
        print("    ...")


if __name__ == '__main__':
    main()

