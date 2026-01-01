# -*- coding: utf-8 -*-
"""
Lock PC
Locks the Windows workstation immediately
"""
import ctypes
import subprocess

print("=" * 50)
print("   LOCKING PC")
print("=" * 50)

try:
    # Method 1: Using ctypes (most reliable)
    ctypes.windll.user32.LockWorkStation()
    print("[OK] PC locked successfully!")
except Exception as e:
    print(f"[!] Ctypes method failed: {e}")
    print("[*] Trying alternative method...")
    
    try:
        # Method 2: Using rundll32
        subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=True)
        print("[OK] PC locked successfully!")
    except Exception as e2:
        print(f"[ERROR] Failed to lock PC: {e2}")

