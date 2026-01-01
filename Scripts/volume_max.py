# -*- coding: utf-8 -*-
"""
Volume Max
Sets system volume to 100% and unmutes
"""
import subprocess
import ctypes
from ctypes import POINTER, cast

print("=" * 50)
print("   VOLUME MAX")
print("=" * 50)

# Method 1: Using pycaw if available
try:
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Unmute
    volume.SetMute(0, None)
    
    # Set to 100%
    volume.SetMasterVolumeLevelScalar(1.0, None)
    
    print("[OK] Volume set to 100% using pycaw")
    
except ImportError:
    print("[*] pycaw not installed, using alternative method...")
    
    # Method 2: Using nircmd or PowerShell
    try:
        # PowerShell method
        ps_script = '''
        $obj = New-Object -ComObject WScript.Shell
        # Press volume up key many times
        1..50 | ForEach-Object { $obj.SendKeys([char]175) }
        '''
        subprocess.run(['powershell', '-Command', ps_script], capture_output=True)
        print("[OK] Volume increased using keyboard simulation")
        
    except Exception as e:
        print(f"[!] PowerShell method failed: {e}")
        
        # Method 3: Direct key simulation
        try:
            VK_VOLUME_UP = 0xAF
            VK_VOLUME_MUTE = 0xAD
            
            user32 = ctypes.windll.user32
            
            # Unmute first
            user32.keybd_event(VK_VOLUME_MUTE, 0, 0, 0)
            user32.keybd_event(VK_VOLUME_MUTE, 0, 2, 0)
            
            # Press volume up 50 times
            for _ in range(50):
                user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
                user32.keybd_event(VK_VOLUME_UP, 0, 2, 0)
            
            print("[OK] Volume increased using keybd_event")
            
        except Exception as e2:
            print(f"[ERROR] {e2}")

# Play a test sound
print("\n[*] Playing test sound...")
try:
    import winsound
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    print("[OK] Test sound played")
except:
    print("[!] Could not play test sound")

print("\n" + "=" * 50)
print("[OK] Volume should now be at maximum!")
print("=" * 50)

