# -*- coding: utf-8 -*-
"""
Restart PC
Restarts the Windows PC
"""
import subprocess
import os

# Get delay from environment variable (default: 30 seconds)
DELAY = os.environ.get("RESTART_DELAY", "30")
FORCE = os.environ.get("RESTART_FORCE", "false").lower() == "true"

print("=" * 50)
print("   RESTART PC")
print("=" * 50)
print(f"   Delay: {DELAY} seconds")
print(f"   Force close apps: {FORCE}")
print("=" * 50)

try:
    # Build restart command
    cmd = ['shutdown', '/r', f'/t', DELAY]
    
    if FORCE:
        cmd.append('/f')  # Force close applications
    
    cmd.extend(['/c', 'System restart initiated by remote command'])
    
    subprocess.run(cmd, check=True)
    print(f"\n[OK] Restart scheduled in {DELAY} seconds")
    print("    To abort: Run 'shutdown /a' in command prompt")
    
except Exception as e:
    print(f"\n[ERROR] Failed to restart: {e}")

