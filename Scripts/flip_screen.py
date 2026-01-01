# -*- coding: utf-8 -*-
"""
Flip Screen
Rotates the display - toggle between normal and flipped
"""
import subprocess
import os

# Action: toggle, flip, normal, left, right
ACTION = os.environ.get("SCREEN_ACTION", "toggle").lower()

print("=" * 50)
print("   FLIP SCREEN")
print("=" * 50)
print("   Action: %s" % ACTION)
print("=" * 50)

# Display orientation constants
DMDO_DEFAULT = 0    # Normal
DMDO_90 = 1         # 90 degrees
DMDO_180 = 2        # 180 degrees (upside down)
DMDO_270 = 3        # 270 degrees

orientation_names = {
    0: 'Normal (0)',
    1: '90 Right',
    2: '180 Flipped',
    3: '270 Left'
}

def get_current_orientation():
    """Get current screen orientation."""
    ps_script = '''
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class Display {
    [DllImport("user32.dll")]
    public static extern bool EnumDisplaySettings(string deviceName, int modeNum, ref DEVMODE devMode);
    
    public const int ENUM_CURRENT_SETTINGS = -1;
    
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct DEVMODE {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmDeviceName;
        public short dmSpecVersion;
        public short dmDriverVersion;
        public short dmSize;
        public short dmDriverExtra;
        public int dmFields;
        public int dmPositionX;
        public int dmPositionY;
        public int dmDisplayOrientation;
        public int dmDisplayFixedOutput;
        public short dmColor;
        public short dmDuplex;
        public short dmYResolution;
        public short dmTTOption;
        public short dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public short dmLogPixels;
        public int dmBitsPerPel;
        public int dmPelsWidth;
        public int dmPelsHeight;
        public int dmDisplayFlags;
        public int dmDisplayFrequency;
        public int dmICMMethod;
        public int dmICMIntent;
        public int dmMediaType;
        public int dmDitherType;
        public int dmReserved1;
        public int dmReserved2;
        public int dmPanningWidth;
        public int dmPanningHeight;
    }
    
    public static int GetOrientation() {
        DEVMODE dm = new DEVMODE();
        dm.dmSize = (short)Marshal.SizeOf(typeof(DEVMODE));
        if (EnumDisplaySettings(null, ENUM_CURRENT_SETTINGS, ref dm)) {
            return dm.dmDisplayOrientation;
        }
        return -1;
    }
}
"@ -ErrorAction SilentlyContinue

[Display]::GetOrientation()
'''
    
    result = subprocess.run(
        ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
        capture_output=True,
        text=True
    )
    
    try:
        return int(result.stdout.strip())
    except:
        return 0

def set_orientation(orientation):
    """Set screen orientation."""
    ps_script = '''
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class DisplaySettings {
    [DllImport("user32.dll")]
    public static extern bool EnumDisplaySettings(string deviceName, int modeNum, ref DEVMODE devMode);
    
    [DllImport("user32.dll")]
    public static extern int ChangeDisplaySettings(ref DEVMODE devMode, int flags);
    
    public const int ENUM_CURRENT_SETTINGS = -1;
    public const int CDS_UPDATEREGISTRY = 0x01;
    
    [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]
    public struct DEVMODE {
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmDeviceName;
        public short dmSpecVersion;
        public short dmDriverVersion;
        public short dmSize;
        public short dmDriverExtra;
        public int dmFields;
        public int dmPositionX;
        public int dmPositionY;
        public int dmDisplayOrientation;
        public int dmDisplayFixedOutput;
        public short dmColor;
        public short dmDuplex;
        public short dmYResolution;
        public short dmTTOption;
        public short dmCollate;
        [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
        public string dmFormName;
        public short dmLogPixels;
        public int dmBitsPerPel;
        public int dmPelsWidth;
        public int dmPelsHeight;
        public int dmDisplayFlags;
        public int dmDisplayFrequency;
        public int dmICMMethod;
        public int dmICMIntent;
        public int dmMediaType;
        public int dmDitherType;
        public int dmReserved1;
        public int dmReserved2;
        public int dmPanningWidth;
        public int dmPanningHeight;
    }
    
    public static int Rotate(int orientation) {
        DEVMODE dm = new DEVMODE();
        dm.dmSize = (short)Marshal.SizeOf(typeof(DEVMODE));
        
        if (EnumDisplaySettings(null, ENUM_CURRENT_SETTINGS, ref dm)) {
            int temp;
            if ((dm.dmDisplayOrientation %% 2) != (orientation %% 2)) {
                temp = dm.dmPelsWidth;
                dm.dmPelsWidth = dm.dmPelsHeight;
                dm.dmPelsHeight = temp;
            }
            dm.dmDisplayOrientation = orientation;
            return ChangeDisplaySettings(ref dm, CDS_UPDATEREGISTRY);
        }
        return -1;
    }
}
"@ -ErrorAction SilentlyContinue

[DisplaySettings]::Rotate(%d)
''' % orientation
    
    result = subprocess.run(
        ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
        capture_output=True,
        text=True
    )
    
    return '0' in result.stdout or result.returncode == 0

try:
    # Get current orientation
    current = get_current_orientation()
    print("[*] Current orientation: %s" % orientation_names.get(current, 'Unknown'))
    
    # Determine target orientation
    if ACTION == "toggle":
        # Toggle between normal and flipped
        if current == DMDO_DEFAULT:
            target = DMDO_180
        else:
            target = DMDO_DEFAULT
    elif ACTION == "flip" or ACTION == "180":
        target = DMDO_180
    elif ACTION == "normal" or ACTION == "0":
        target = DMDO_DEFAULT
    elif ACTION == "left" or ACTION == "270":
        target = DMDO_270
    elif ACTION == "right" or ACTION == "90":
        target = DMDO_90
    else:
        target = DMDO_180
    
    print("[*] Target orientation: %s" % orientation_names.get(target, 'Unknown'))
    
    if current == target:
        print("\n[!] Already at target orientation!")
    else:
        if set_orientation(target):
            print("\n[OK] Screen rotated to: %s" % orientation_names.get(target, 'Unknown'))
        else:
            print("\n[!] Failed to rotate screen")

except Exception as e:
    print("[ERROR] %s" % str(e))

print("\n" + "=" * 50)
