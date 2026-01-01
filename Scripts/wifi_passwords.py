# -*- coding: utf-8 -*-
"""Extract all saved WiFi passwords"""
import subprocess
import re
import sys

def safe_str(s):
    """Convert string to ASCII-safe version"""
    if s is None:
        return ""
    try:
        return s.encode('ascii', 'replace').decode('ascii')
    except:
        return str(s).encode('ascii', 'replace').decode('ascii')

def safe_print(msg):
    """Print with ASCII-safe encoding"""
    try:
        print(safe_str(msg))
    except:
        print(msg.encode('ascii', 'replace').decode('ascii'))

safe_print("=" * 60)
safe_print("   WIFI PASSWORD EXTRACTOR")
safe_print("=" * 60)
safe_print("")

# Get all WiFi profiles
result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, encoding='utf-8', errors='replace')
profiles = re.findall(r"All User Profile\s*:\s*(.*)", result.stdout)

if not profiles:
    profiles = re.findall(r"Profil utilisateur\s*:\s*(.*)", result.stdout)

wifi_data = []

for profile in profiles:
    profile = profile.strip()
    # Get password for each profile
    result = subprocess.run(
        ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    
    password = re.search(r"Key Content\s*:\s*(.*)", result.stdout)
    if not password:
        password = re.search(r"Contenu de la cl.*:\s*(.*)", result.stdout)
    
    pwd = password.group(1).strip() if password else "No password / Open network"
    wifi_data.append((profile, pwd))
    
    safe_print("[WiFi] Network: %s" % safe_str(profile))
    safe_print("       Password: %s" % safe_str(pwd))
    safe_print("-" * 40)

safe_print("")
safe_print("[OK] Found %d saved WiFi networks!" % len(wifi_data))
