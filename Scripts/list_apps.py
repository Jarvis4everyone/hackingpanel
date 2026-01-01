# -*- coding: utf-8 -*-
"""
List All Installed Applications
Returns a list of all installed programs with their executable paths
"""
import os
import subprocess
import json
from datetime import datetime

def get_installed_apps():
    """Get installed apps with executable paths from Windows Registry."""
    apps = []
    
    ps_script = '''
$apps = @()

# Exclusion patterns for exe files (installers, uninstallers, updaters)
$excludePatterns = @('uninstall', 'uninst', 'setup', 'installer', 'update', 'updater', 'helper', 'crash', 'reporter')

function Should-ExcludeExe {
    param($exeName)
    $lowerName = $exeName.ToLower()
    foreach ($pattern in $excludePatterns) {
        if ($lowerName -like "*$pattern*") { return $true }
    }
    return $false
}

function Get-BestExe {
    param($folder, $appName)
    
    if (-not $folder -or -not (Test-Path $folder -ErrorAction SilentlyContinue)) { return $null }
    
    $exes = Get-ChildItem -Path $folder -Filter "*.exe" -Recurse -Depth 2 -ErrorAction SilentlyContinue | 
            Where-Object { -not (Should-ExcludeExe $_.Name) } |
            Select-Object -First 20
    
    if (-not $exes) { return $null }
    
    # Clean app name for matching
    $appWords = ($appName -replace '[^a-zA-Z0-9 ]', ' ') -split '\s+' | Where-Object { $_.Length -gt 2 }
    
    # Priority 1: Exact name match
    foreach ($exe in $exes) {
        $baseName = $exe.BaseName.ToLower()
        $appLower = $appName.ToLower() -replace '[^a-zA-Z0-9]', ''
        $baseClean = $baseName -replace '[^a-zA-Z0-9]', ''
        if ($baseClean -eq $appLower) { return $exe.FullName }
    }
    
    # Priority 2: Contains main app word
    foreach ($exe in $exes) {
        $baseName = $exe.BaseName.ToLower()
        foreach ($word in $appWords) {
            if ($word.Length -gt 3 -and $baseName -like "*$($word.ToLower())*") {
                return $exe.FullName
            }
        }
    }
    
    # Priority 3: First non-excluded exe in root folder
    $rootExes = Get-ChildItem -Path $folder -Filter "*.exe" -ErrorAction SilentlyContinue | 
                Where-Object { -not (Should-ExcludeExe $_.Name) } |
                Select-Object -First 1
    if ($rootExes) { return $rootExes.FullName }
    
    # Fallback: First exe found
    return $exes[0].FullName
}

function Get-AppLocation {
    param($regKey)
    
    # Try InstallLocation
    if ($regKey.InstallLocation -and (Test-Path $regKey.InstallLocation -ErrorAction SilentlyContinue)) {
        return $regKey.InstallLocation
    }
    
    # Try DisplayIcon path
    if ($regKey.DisplayIcon) {
        $iconPath = $regKey.DisplayIcon -replace ',.*$', '' -replace '"', ''
        if ($iconPath -match '\\.exe$') {
            $dir = Split-Path $iconPath -Parent
            if (Test-Path $dir -ErrorAction SilentlyContinue) { return $dir }
        }
    }
    
    # Try UninstallString path
    if ($regKey.UninstallString) {
        $uninstall = $regKey.UninstallString -replace '"', ''
        if ($uninstall -match '^(.+)\\\\[^\\\\]+\\.exe') {
            $dir = $matches[1]
            if (Test-Path $dir -ErrorAction SilentlyContinue) { return $dir }
        }
    }
    
    return $null
}

function Get-ExeFromDisplayIcon {
    param($regKey)
    
    if ($regKey.DisplayIcon) {
        $iconPath = $regKey.DisplayIcon -replace ',.*$', '' -replace '"', ''
        if ($iconPath -match '\\.exe$' -and (Test-Path $iconPath -ErrorAction SilentlyContinue)) {
            if (-not (Should-ExcludeExe (Split-Path $iconPath -Leaf))) {
                return $iconPath
            }
        }
    }
    return $null
}

# Registry paths
$paths = @(
    "HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
    "HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*",
    "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*"
)

foreach ($regPath in $paths) {
    if (Test-Path $regPath) {
        Get-ItemProperty $regPath -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName } | ForEach-Object {
            $name = $_.DisplayName
            $location = Get-AppLocation $_
            $exe = $null
            
            # Try DisplayIcon first (most reliable)
            $exe = Get-ExeFromDisplayIcon $_
            
            # If not found, search in location folder
            if (-not $exe -and $location) {
                $exe = Get-BestExe $location $name
            }
            
            $apps += [PSCustomObject]@{
                Name = $name
                Location = if ($location) { $location } else { "" }
                Executable = if ($exe) { $exe } else { "" }
            }
        }
    }
}

$apps | Sort-Object Name -Unique | ConvertTo-Json -Depth 3
'''
    
    try:
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=180
        )
        
        if result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, dict):
                data = [data]
            
            for app in data:
                if app.get('Name'):
                    apps.append({
                        'name': app.get('Name', ''),
                        'location': app.get('Location', ''),
                        'executable': app.get('Executable', '')
                    })
    except json.JSONDecodeError as e:
        print("JSON Error: %s" % str(e))
    except Exception as e:
        print("Error: %s" % str(e))
    
    return apps


def main():
    print("=" * 70)
    print("   INSTALLED APPLICATIONS")
    print("=" * 70)
    print("   Scan Time: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)
    
    print("")
    print("[*] Scanning installed applications (this may take a moment)...")
    
    apps = get_installed_apps()
    
    # Remove duplicates and sort
    seen = set()
    unique_apps = []
    for app in apps:
        key = app['name'].lower()
        if key not in seen:
            seen.add(key)
            unique_apps.append(app)
    
    unique_apps.sort(key=lambda x: x['name'].lower())
    
    print("[*] Found %d applications" % len(unique_apps))
    print("")
    print("=" * 70)
    print("   APPLICATION LIST")
    print("=" * 70)
    
    apps_with_exe = []
    apps_without_exe = []
    
    for app in unique_apps:
        if app['executable']:
            apps_with_exe.append(app)
        else:
            apps_without_exe.append(app)
    
    # Print apps with executables first
    print("")
    print("[LAUNCHABLE APPLICATIONS] (%d apps)" % len(apps_with_exe))
    print("-" * 70)
    for i, app in enumerate(apps_with_exe, 1):
        print("")
        print("%d. %s" % (i, app['name']))
        print("   Path: %s" % app['executable'])
    
    # Print apps without executables
    if apps_without_exe:
        print("")
        print("")
        print("[SYSTEM COMPONENTS / NO EXECUTABLE FOUND] (%d items)" % len(apps_without_exe))
        print("-" * 70)
        for app in apps_without_exe:
            loc = app['location'] if app['location'] else "System component"
            print("   - %s (%s)" % (app['name'], loc))
    
    print("")
    print("=" * 70)
    print("[OK] Total: %d applications (%d launchable)" % (len(unique_apps), len(apps_with_exe)))
    print("=" * 70)


if __name__ == '__main__':
    main()
