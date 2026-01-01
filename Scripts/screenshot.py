# -*- coding: utf-8 -*-
"""Take a screenshot and upload to server"""
import subprocess
import os
import sys
from datetime import datetime
import base64
import urllib.request
import urllib.parse
import json

# SERVER_URL will be injected by the server when sending the script
try:
    SERVER_URL
except NameError:
    print("ERROR: SERVER_URL not set. Server should inject this variable.")
    sys.exit(1)
PC_ID = os.environ.get("CC_PC_ID", "unknown")

# Create screenshot filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
temp_file = os.path.join(os.environ.get('TEMP', '.'), f'screenshot_{timestamp}.png')

# Take screenshot using PowerShell
ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
$bitmap.Save("{temp_file}")
$graphics.Dispose()
$bitmap.Dispose()
'''

result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)

if os.path.exists(temp_file):
    print(f"Screenshot saved: {temp_file}")
    print(f"Size: {os.path.getsize(temp_file)} bytes")
    
    # Try to upload to server
    try:
        with open(temp_file, 'rb') as f:
            content = base64.b64encode(f.read()).decode('utf-8')
        
        data = json.dumps({
            "pc_id": PC_ID,
            "filename": f"screenshot_{timestamp}.png",
            "content_base64": content,
            "original_path": temp_file
        }).encode('utf-8')
        
        req = urllib.request.Request(
            f"{SERVER_URL}/upload/base64",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            print(f"Uploaded to server: {result}")
    except Exception as e:
        print(f"Upload failed (file saved locally): {e}")
    
    # Clean up temp file
    try:
        os.remove(temp_file)
    except:
        pass
else:
    print("Failed to take screenshot")
    print(result.stderr if result.stderr else "Unknown error")
