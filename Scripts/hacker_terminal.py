# -*- coding: utf-8 -*-
"""Matrix Rain Effect - Opens 10 terminal windows with green matrix effect"""
import subprocess
import os
import sys
import tempfile
import time

# Get settings from environment variables
duration = int(os.environ.get("MATRIX_DURATION", "15"))
num_terminals = int(os.environ.get("MATRIX_TERMINALS", "10"))
message = os.environ.get("MATRIX_MESSAGE", "YOUR PC HAS BEEN HACKED! CONGRATS!")

print("[*] MATRIX RAIN ATTACK")
print(f"[*] Opening {num_terminals} terminal windows...")
print(f"[*] Duration: {duration} seconds each")
print(f"[*] Message: {message}")
print("[*] Launching terminals (non-blocking)...")

# Create the matrix rain script that will run in each terminal
matrix_script = f'''
import random
import time
import os
import sys

# Set console to green on black
os.system('color 0a')
os.system('mode con: cols=100 lines=35')

chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
katakana = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
all_chars = chars + katakana

try:
    width = os.get_terminal_size().columns
except:
    width = 100

columns = [0] * width

start = time.time()
duration = {duration}

try:
    while time.time() - start < duration:
        line = ""
        for i in range(width):
            if random.random() > 0.95:
                columns[i] = random.randint(5, 20)
            
            if columns[i] > 0:
                line += random.choice(all_chars)
                columns[i] -= 1
            else:
                line += " "
        
        print(line)
        time.sleep(0.03)
except KeyboardInterrupt:
    pass

# Show the hacked message
os.system('cls')
os.system('color 0c')  # Red on black

message = "{message}"
width = 100

print()
print()
print("=" * width)
print()
print(" " * ((width - len(message)) // 2) + message)
print()
print("=" * width)
print()
print()

# Dramatic effect
for i in range(3):
    time.sleep(0.3)
    os.system('color 0a')  # Green
    time.sleep(0.3)
    os.system('color 0c')  # Red

time.sleep(2)
# Terminal will close automatically
'''

# Write the script to temp files (one for each terminal to avoid conflicts)
temp_files = []
for i in range(num_terminals):
    temp_file = os.path.join(tempfile.gettempdir(), f"matrix_rain_{i}.py")
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(matrix_script)
    temp_files.append(temp_file)

# Launch terminals independently (non-blocking)
# Using 'start' with /B flag would hide window, so we use regular start
# Each terminal runs independently and closes when done

for i in range(num_terminals):
    # Use subprocess.Popen with shell=True and don't wait
    # The /C flag makes cmd close after the command finishes
    cmd = f'start "Hacker Terminal {i+1}" cmd /C "color 0a && python "{temp_files[i]}""'
    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[+] Terminal {i+1}/{num_terminals} launched")
    time.sleep(1)  # 1 second delay between each terminal

print()
print("[OK] All terminals launched!")
print(f"[*] Each will run for {duration} seconds then show message and close")
print("[*] This script is done - terminals run independently")
