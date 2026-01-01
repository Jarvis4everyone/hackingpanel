# -*- coding: utf-8 -*-
"""Get current clipboard content"""
import subprocess

print("="*60)
print("   CLIPBOARD CONTENT")
print("="*60 + "\n")

ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
$clipboard = [System.Windows.Forms.Clipboard]::GetText()
if ($clipboard) {
    Write-Output $clipboard
} else {
    Write-Output "[Clipboard is empty or contains non-text data]"
}
'''

result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True, encoding='utf-8', errors='replace')

print("[CURRENT CLIPBOARD CONTENT]")
print("-" * 40)
content = result.stdout.strip()
if len(content) > 500:
    print(content[:500] + "...")
    print(f"\n(Truncated - Full length: {len(content)} characters)")
else:
    print(content)
print("-" * 40)

print("\n[OK] Clipboard content captured!")

