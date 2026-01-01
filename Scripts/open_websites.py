# -*- coding: utf-8 -*-
"""Open websites in the default browser"""
import webbrowser
import os
import time

# Get URLs from environment variable (comma-separated) or use defaults
urls_input = os.environ.get("WEBSITES", "https://www.google.com,https://www.youtube.com,https://www.github.com")

# Parse URLs (comma-separated)
urls = [url.strip() for url in urls_input.split(",") if url.strip()]

print("[*] OPEN WEBSITES")
print(f"[*] URLs to open: {len(urls)}")
print("=" * 50)

for i, url in enumerate(urls, 1):
    # Add https:// if missing
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    
    print(f"[{i}] Opening: {url}")
    try:
        webbrowser.open(url)
        time.sleep(0.5)  # Small delay between openings
    except Exception as e:
        print(f"    ERROR: {e}")

print("=" * 50)
print(f"\n[OK] Opened {len(urls)} website(s) in default browser!")

