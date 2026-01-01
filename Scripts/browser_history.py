"""
Browser History Extractor
Extracts browsing history from Chrome, Firefox, and Edge
"""
import os
import sys
import json
import sqlite3
import shutil
import tempfile
from datetime import datetime, timedelta

# Fix Unicode encoding issues on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

def safe_str(s):
    """Convert string to safe ASCII representation."""
    if s is None:
        return "None"
    try:
        return str(s).encode('ascii', 'replace').decode('ascii')
    except:
        return str(s)

def safe_print(msg):
    """Print with Unicode-safe encoding."""
    try:
        print(str(msg).encode('ascii', 'replace').decode('ascii'))
    except:
        try:
            print(str(msg))
        except:
            pass

def get_chrome_history():
    """Extract Chrome browsing history."""
    history = []
    
    # Chrome history paths
    paths = [
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History'),
        os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data\Profile 1\History'),
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                # Copy to temp file (Chrome locks the file)
                temp_file = os.path.join(tempfile.gettempdir(), 'chrome_history_temp')
                shutil.copy2(path, temp_file)
                
                conn = sqlite3.connect(temp_file)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT url, title, visit_count, last_visit_time
                    FROM urls
                    ORDER BY last_visit_time DESC
                    LIMIT 500
                ''')
                
                for row in cursor.fetchall():
                    url, title, visit_count, last_visit = row
                    # Chrome timestamps are microseconds since Jan 1, 1601
                    if last_visit:
                        timestamp = datetime(1601, 1, 1) + timedelta(microseconds=last_visit)
                        last_visit_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        last_visit_str = 'Unknown'
                    
                    history.append({
                        'browser': 'Chrome',
                        'url': url or 'No URL',
                        'title': title or 'No title',
                        'visits': visit_count,
                        'last_visit': last_visit_str
                    })
                
                conn.close()
                os.remove(temp_file)
            except Exception as e:
                safe_print(f"Chrome error: {e}")
    
    return history


def get_firefox_history():
    """Extract Firefox browsing history."""
    history = []
    
    firefox_path = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
    
    if os.path.exists(firefox_path):
        for profile in os.listdir(firefox_path):
            db_path = os.path.join(firefox_path, profile, 'places.sqlite')
            if os.path.exists(db_path):
                try:
                    temp_file = os.path.join(tempfile.gettempdir(), 'firefox_history_temp')
                    shutil.copy2(db_path, temp_file)
                    
                    conn = sqlite3.connect(temp_file)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        SELECT url, title, visit_count, last_visit_date
                        FROM moz_places
                        WHERE visit_count > 0
                        ORDER BY last_visit_date DESC
                        LIMIT 500
                    ''')
                    
                    for row in cursor.fetchall():
                        url, title, visit_count, last_visit = row
                        if last_visit:
                            # Firefox timestamps are microseconds since epoch
                            timestamp = datetime.fromtimestamp(last_visit / 1000000)
                            last_visit_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            last_visit_str = 'Unknown'
                        
                        history.append({
                            'browser': 'Firefox',
                            'url': url or 'No URL',
                            'title': title or 'No title',
                            'visits': visit_count,
                            'last_visit': last_visit_str
                        })
                    
                    conn.close()
                    os.remove(temp_file)
                except Exception as e:
                    safe_print(f"Firefox error: {e}")
    
    return history


def get_edge_history():
    """Extract Edge browsing history."""
    history = []
    
    paths = [
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History'),
        os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Profile 1\History'),
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                temp_file = os.path.join(tempfile.gettempdir(), 'edge_history_temp')
                shutil.copy2(path, temp_file)
                
                conn = sqlite3.connect(temp_file)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT url, title, visit_count, last_visit_time
                    FROM urls
                    ORDER BY last_visit_time DESC
                    LIMIT 500
                ''')
                
                for row in cursor.fetchall():
                    url, title, visit_count, last_visit = row
                    if last_visit:
                        timestamp = datetime(1601, 1, 1) + timedelta(microseconds=last_visit)
                        last_visit_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        last_visit_str = 'Unknown'
                    
                    history.append({
                        'browser': 'Edge',
                        'url': url or 'No URL',
                        'title': title or 'No title',
                        'visits': visit_count,
                        'last_visit': last_visit_str
                    })
                
                conn.close()
                os.remove(temp_file)
            except Exception as e:
                safe_print(f"Edge error: {e}")
    
    return history


def main():
    safe_print("=" * 60)
    safe_print("BROWSER HISTORY EXTRACTOR")
    safe_print("=" * 60)
    
    all_history = []
    
    safe_print("\n[*] Extracting Chrome history...")
    chrome_history = get_chrome_history()
    all_history.extend(chrome_history)
    safe_print(f"    Found {len(chrome_history)} entries")
    
    safe_print("\n[*] Extracting Firefox history...")
    firefox_history = get_firefox_history()
    all_history.extend(firefox_history)
    safe_print(f"    Found {len(firefox_history)} entries")
    
    safe_print("\n[*] Extracting Edge history...")
    edge_history = get_edge_history()
    all_history.extend(edge_history)
    safe_print(f"    Found {len(edge_history)} entries")
    
    safe_print(f"\n[*] Total entries: {len(all_history)}")
    
    # Sort by last visit
    all_history.sort(key=lambda x: x['last_visit'], reverse=True)
    
    # Print results
    safe_print("\n" + "=" * 60)
    safe_print("RECENT BROWSING HISTORY (Last 100)")
    safe_print("=" * 60)
    
    for i, entry in enumerate(all_history[:100], 1):
        title = safe_str(entry['title'])[:60]
        url = safe_str(entry['url'])[:80]
        safe_print(f"\n{i}. [{entry['browser']}] {entry['last_visit']}")
        safe_print(f"   Title: {title}...")
        safe_print(f"   URL: {url}...")
        safe_print(f"   Visits: {entry['visits']}")
    
    # Save full report
    report_path = os.path.join(tempfile.gettempdir(), 'browser_history_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(all_history, f, indent=2, ensure_ascii=False)
    
    safe_print(f"\n[*] Full report saved to: {report_path}")
    safe_print(f"[*] Total unique URLs: {len(set(h['url'] for h in all_history))}")


if __name__ == '__main__':
    main()

