# -*- coding: utf-8 -*-
"""
Email Accounts Finder
Lists configured email accounts from various sources
"""
import subprocess
import os
import winreg
import json
from datetime import datetime

print("=" * 70)
print("   EMAIL ACCOUNTS FINDER")
print("=" * 70)
print(f"   Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

email_accounts = []

# Windows Mail App accounts
print("\n[*] WINDOWS MAIL ACCOUNTS")
print("-" * 50)

mail_path = os.path.expandvars(r'%LOCALAPPDATA%\Packages\microsoft.windowscommunicationsapps_8wekyb3d8bbwe\LocalState\Indexed\LiveComm')

if os.path.exists(mail_path):
    try:
        for root, dirs, files in os.walk(mail_path):
            for file in files:
                if file.endswith('.eml') or 'account' in file.lower():
                    print(f"    Found: {file}")
    except Exception as e:
        print(f"    [!] Error: {e}")
else:
    print("    Windows Mail not configured")

# Outlook profiles from registry
print("\n[*] OUTLOOK PROFILES")
print("-" * 50)

outlook_paths = [
    r"Software\Microsoft\Office\16.0\Outlook\Profiles",
    r"Software\Microsoft\Office\15.0\Outlook\Profiles",
    r"Software\Microsoft\Windows NT\CurrentVersion\Windows Messaging Subsystem\Profiles",
]

for path in outlook_paths:
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        i = 0
        while True:
            try:
                profile_name = winreg.EnumKey(key, i)
                print(f"    Profile: {profile_name}")
                email_accounts.append({'type': 'Outlook', 'profile': profile_name})
                i += 1
            except WindowsError:
                break
        winreg.CloseKey(key)
    except:
        pass

if not email_accounts:
    print("    No Outlook profiles found")

# Thunderbird profiles
print("\n[*] THUNDERBIRD PROFILES")
print("-" * 50)

thunderbird_path = os.path.expandvars(r'%APPDATA%\Thunderbird\Profiles')

if os.path.exists(thunderbird_path):
    profiles = os.listdir(thunderbird_path)
    for profile in profiles:
        profile_path = os.path.join(thunderbird_path, profile)
        prefs_file = os.path.join(profile_path, 'prefs.js')
        
        if os.path.exists(prefs_file):
            print(f"    Profile: {profile}")
            
            # Try to extract email from prefs
            try:
                with open(prefs_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Look for email addresses
                    import re
                    emails = re.findall(r'user_pref\("mail\.identity\..*?\.useremail",\s*"([^"]+)"', content)
                    for email in emails:
                        print(f"      Email: {email}")
                        email_accounts.append({'type': 'Thunderbird', 'email': email})
            except:
                pass
else:
    print("    Thunderbird not installed")

# Browser saved emails (from autofill)
print("\n[*] BROWSER AUTOFILL EMAILS")
print("-" * 50)

# Chrome Web Data
chrome_path = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Web Data')

if os.path.exists(chrome_path):
    import sqlite3
    import shutil
    import tempfile
    
    try:
        # Copy to temp (Chrome locks the file)
        temp_db = os.path.join(tempfile.gettempdir(), 'chrome_webdata_temp')
        shutil.copy2(chrome_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Get autofill emails
        cursor.execute("SELECT value FROM autofill WHERE name LIKE '%email%' OR value LIKE '%@%'")
        
        seen = set()
        for row in cursor.fetchall():
            value = row[0]
            if '@' in value and value not in seen:
                print(f"    Chrome: {value}")
                email_accounts.append({'type': 'Chrome Autofill', 'email': value})
                seen.add(value)
        
        conn.close()
        os.remove(temp_db)
    except Exception as e:
        print(f"    [!] Chrome error: {e}")
else:
    print("    Chrome not found or no autofill data")

# Credential Manager emails
print("\n[*] WINDOWS CREDENTIAL MANAGER")
print("-" * 50)

ps_creds = '''
$creds = cmdkey /list 2>$null
$creds | Select-String -Pattern "Target:|User:" | ForEach-Object { $_.Line.Trim() }
'''

result = subprocess.run(
    ['powershell', '-Command', ps_creds],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)

if result.stdout.strip():
    lines = result.stdout.strip().split('\n')
    for line in lines[:20]:  # Limit output
        if '@' in line or 'mail' in line.lower() or 'outlook' in line.lower():
            print(f"    {line}")
else:
    print("    No relevant credentials found")

# Summary
print("\n" + "=" * 70)
print(f"[OK] Found {len(email_accounts)} email account references")
print("=" * 70)

