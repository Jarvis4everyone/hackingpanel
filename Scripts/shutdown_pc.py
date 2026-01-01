# -*- coding: utf-8 -*-
"""
Shutdown PC
Shuts down the Windows PC
"""
import subprocess
import os

# Get delay from environment variable (default: 30 seconds)
DELAY = os.environ.get("SHUTDOWN_DELAY", "30")
FORCE = os.environ.get("SHUTDOWN_FORCE", "false").lower() == "true"

print("=" * 50)
print("   SHUTDOWN PC")
print("=" * 50)
print(f"   Delay: {DELAY} seconds")
print(f"   Force close apps: {FORCE}")
print("=" * 50)

try:
    # Build shutdown command
    cmd = ['shutdown', '/s', f'/t', DELAY]
    
    if FORCE:
        cmd.append('/f')  # Force close applications
    
    cmd.extend(['/c', 'System shutdown initiated by remote command'])
    
    subprocess.run(cmd, check=True)
    print(f"\n[OK] Shutdown scheduled in {DELAY} seconds")
    print("    To abort: Run 'shutdown /a' in command prompt")
    
except Exception as e:
    print(f"\n[ERROR] Failed to shutdown: {e}")

