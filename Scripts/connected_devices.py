# -*- coding: utf-8 -*-
"""
Connected Devices Scanner
Lists all USB, Bluetooth, and network devices
"""
import subprocess
import os
from datetime import datetime

print("=" * 70)
print("   CONNECTED DEVICES SCANNER")
print("=" * 70)
print(f"   Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

# USB Devices
print("\n[*] USB DEVICES")
print("-" * 50)

ps_usb = '''
Get-PnpDevice -Class USB -Status OK | Select-Object FriendlyName, Status, InstanceId | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_usb],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No USB devices found")

# USB Storage History
print("\n[*] USB STORAGE HISTORY")
print("-" * 50)

ps_usb_history = '''
Get-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\*\\*" -ErrorAction SilentlyContinue | 
Select-Object FriendlyName | Where-Object { $_.FriendlyName } | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_usb_history],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No USB storage history")

# Bluetooth Devices
print("\n[*] BLUETOOTH DEVICES")
print("-" * 50)

ps_bluetooth = '''
Get-PnpDevice -Class Bluetooth -ErrorAction SilentlyContinue | 
Select-Object FriendlyName, Status | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_bluetooth],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No Bluetooth devices found")

# Network Adapters
print("\n[*] NETWORK ADAPTERS")
print("-" * 50)

ps_network = '''
Get-NetAdapter | Select-Object Name, Status, MacAddress, LinkSpeed | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_network],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No network adapters found")

# Audio Devices
print("\n[*] AUDIO DEVICES")
print("-" * 50)

ps_audio = '''
Get-PnpDevice -Class AudioEndpoint -Status OK -ErrorAction SilentlyContinue | 
Select-Object FriendlyName, Status | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_audio],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No audio devices found")

# Display Devices
print("\n[*] DISPLAY/MONITOR")
print("-" * 50)

ps_display = '''
Get-PnpDevice -Class Monitor -Status OK -ErrorAction SilentlyContinue | 
Select-Object FriendlyName, Status | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_display],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No monitors found")

# Printers
print("\n[*] PRINTERS")
print("-" * 50)

ps_printers = '''
Get-Printer -ErrorAction SilentlyContinue | Select-Object Name, PrinterStatus, PortName | Format-Table -AutoSize
'''

result = subprocess.run(
    ['powershell', '-Command', ps_printers],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout if result.stdout.strip() else "    No printers found")

print("\n" + "=" * 70)
print("[OK] Device scan complete!")
print("=" * 70)

