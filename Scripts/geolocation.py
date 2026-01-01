# -*- coding: utf-8 -*-
"""
Geolocation
Get location via IP address geolocation
"""
import subprocess
import json
import urllib.request

print("=" * 60)
print("   GEOLOCATION FINDER")
print("=" * 60)

location_data = {}

# IP-based geolocation
print("\n[*] Getting location via IP address...")
try:
    # Get public IP
    with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=10) as response:
        ip_data = json.loads(response.read().decode())
        public_ip = ip_data.get('ip', 'Unknown')
        location_data['public_ip'] = public_ip
        print(f"    Public IP: {public_ip}")
    
    # Get location from IP
    with urllib.request.urlopen(f"http://ip-api.com/json/{public_ip}", timeout=10) as response:
        geo_data = json.loads(response.read().decode())
        
        location_data['ip_location'] = {
            'country': geo_data.get('country', 'Unknown'),
            'region': geo_data.get('regionName', 'Unknown'),
            'city': geo_data.get('city', 'Unknown'),
            'zip': geo_data.get('zip', 'Unknown'),
            'lat': geo_data.get('lat', 0),
            'lon': geo_data.get('lon', 0),
            'isp': geo_data.get('isp', 'Unknown'),
            'timezone': geo_data.get('timezone', 'Unknown'),
            'source': 'IP-based (approximate)',
            'accuracy': 'APPROXIMATE'
        }
        
        print(f"    Country: {geo_data.get('country')}")
        print(f"    Region: {geo_data.get('regionName')}")
        print(f"    City: {geo_data.get('city')}")
        print(f"    ZIP: {geo_data.get('zip')}")
        print(f"    Coordinates: {geo_data.get('lat')}, {geo_data.get('lon')}")
        print(f"    ISP: {geo_data.get('isp')}")
        print(f"    Timezone: {geo_data.get('timezone')}")
        
        # Google Maps link for IP coordinates
        ip_maps_url = f"https://www.google.com/maps?q={geo_data.get('lat')},{geo_data.get('lon')}"
        location_data['ip_maps_url'] = ip_maps_url
        print(f"\n    Google Maps (IP-based): {ip_maps_url}")
        
except Exception as e:
    print(f"    [!] IP location failed: {e}")

# WiFi networks (for reference)
print("\n[*] Scanning nearby WiFi networks...")
try:
    result = subprocess.run(
        ['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace'
    )
    
    networks = []
    current_network = {}
    
    for line in result.stdout.split('\n'):
        line = line.strip()
        if 'SSID' in line and 'BSSID' not in line:
            if current_network:
                networks.append(current_network)
            current_network = {'ssid': line.split(':')[-1].strip()}
        elif 'BSSID' in line:
            current_network['bssid'] = line.split(':')[-1].strip()
        elif 'Signal' in line:
            current_network['signal'] = line.split(':')[-1].strip()
    
    if current_network:
        networks.append(current_network)
    
    location_data['wifi_networks'] = networks[:10]  # Top 10
    
    print(f"    Found {len(networks)} networks:")
    for i, net in enumerate(networks[:10], 1):
        print(f"    {i}. {net.get('ssid', 'Hidden')} ({net.get('signal', 'N/A')})")
        
except Exception as e:
    print(f"    [!] WiFi scan failed: {e}")

# Summary
print("\n" + "=" * 60)
print("   LOCATION SUMMARY")
print("=" * 60)

# Show IP-based location
if 'ip_location' in location_data:
    loc = location_data['ip_location']
    print(f"\n   [*] IP-Based Location:")
    print(f"   Location: {loc['city']}, {loc['region']}, {loc['country']}")
    print(f"   Coordinates: {loc['lat']}, {loc['lon']}")
    print(f"   ISP: {loc['isp']}")
    print(f"   Timezone: {loc['timezone']}")
    if 'ip_maps_url' in location_data:
        print(f"\n   Google Maps: {location_data['ip_maps_url']}")
        print(f"\n   [OK] Use this link: {location_data.get('ip_maps_url', 'N/A')}")

print("\n" + "=" * 60)

