# -*- coding: utf-8 -*-
"""
Random Sounds
Plays random system sounds at random intervals
"""
import winsound
import random
import time
import os

# Duration in seconds
DURATION = int(os.environ.get("SOUNDS_DURATION", "30"))

print("=" * 50)
print("   RANDOM SOUNDS")
print("=" * 50)
print("   Duration: %d seconds" % DURATION)
print("=" * 50)

# Windows sound files
windows_sounds = [
    r"C:\Windows\Media\Windows Background.wav",
    r"C:\Windows\Media\Windows Balloon.wav",
    r"C:\Windows\Media\Windows Battery Critical.wav",
    r"C:\Windows\Media\Windows Battery Low.wav",
    r"C:\Windows\Media\Windows Critical Stop.wav",
    r"C:\Windows\Media\Windows Default.wav",
    r"C:\Windows\Media\Windows Ding.wav",
    r"C:\Windows\Media\Windows Error.wav",
    r"C:\Windows\Media\Windows Exclamation.wav",
    r"C:\Windows\Media\Windows Feed Discovered.wav",
    r"C:\Windows\Media\Windows Foreground.wav",
    r"C:\Windows\Media\Windows Hardware Fail.wav",
    r"C:\Windows\Media\Windows Hardware Insert.wav",
    r"C:\Windows\Media\Windows Hardware Remove.wav",
    r"C:\Windows\Media\Windows Logoff Sound.wav",
    r"C:\Windows\Media\Windows Logon.wav",
    r"C:\Windows\Media\Windows Menu Command.wav",
    r"C:\Windows\Media\Windows Message Nudge.wav",
    r"C:\Windows\Media\Windows Minimize.wav",
    r"C:\Windows\Media\Windows Notify Calendar.wav",
    r"C:\Windows\Media\Windows Notify Email.wav",
    r"C:\Windows\Media\Windows Notify Messaging.wav",
    r"C:\Windows\Media\Windows Notify System Generic.wav",
    r"C:\Windows\Media\Windows Pop-up Blocked.wav",
    r"C:\Windows\Media\Windows Print complete.wav",
    r"C:\Windows\Media\Windows Proximity Connection.wav",
    r"C:\Windows\Media\Windows Proximity Notification.wav",
    r"C:\Windows\Media\Windows Recycle.wav",
    r"C:\Windows\Media\Windows Restore.wav",
    r"C:\Windows\Media\Windows Ringin.wav",
    r"C:\Windows\Media\Windows Ringout.wav",
    r"C:\Windows\Media\Windows Shutdown.wav",
    r"C:\Windows\Media\Windows Startup.wav",
    r"C:\Windows\Media\Windows Unlock.wav",
    r"C:\Windows\Media\Windows User Account Control.wav",
    r"C:\Windows\Media\chord.wav",
    r"C:\Windows\Media\chimes.wav",
    r"C:\Windows\Media\ding.wav",
    r"C:\Windows\Media\notify.wav",
    r"C:\Windows\Media\tada.wav",
    r"C:\Windows\Media\Ring01.wav",
    r"C:\Windows\Media\Ring02.wav",
    r"C:\Windows\Media\Ring03.wav",
    r"C:\Windows\Media\Alarm01.wav",
    r"C:\Windows\Media\Alarm02.wav",
]

# Filter to only existing files
available_wavs = [f for f in windows_sounds if os.path.exists(f)]

print("[*] Found %d .wav files" % len(available_wavs))

if not available_wavs:
    print("[!] No sound files found!")
    print("[*] Playing system beeps instead...")
    
    start_time = time.time()
    while time.time() - start_time < DURATION:
        freq = random.randint(200, 2000)
        duration_ms = random.randint(100, 500)
        print("    Beep: %d Hz, %d ms" % (freq, duration_ms))
        winsound.Beep(freq, duration_ms)
        time.sleep(random.uniform(0.5, 2.0))
else:
    print("[*] Starting random sounds for %d seconds..." % DURATION)
    print("")
    
    start_time = time.time()
    sound_count = 0
    
    try:
        while time.time() - start_time < DURATION:
            # Pick a random WAV file
            wav_file = random.choice(available_wavs)
            sound_name = os.path.basename(wav_file)
            print("[>] Playing: %s" % sound_name)
            
            try:
                # Play sound synchronously (SND_FILENAME waits for it to finish)
                # Use SND_ASYNC to not block, but add small delay
                winsound.PlaySound(wav_file, winsound.SND_FILENAME)
            except Exception as e:
                print("    Error: %s" % str(e))
            
            sound_count += 1
            
            # Random delay between sounds (0.3 to 1.5 seconds)
            delay = random.uniform(0.3, 1.5)
            time.sleep(delay)
            
            # Check time remaining
            remaining = DURATION - (time.time() - start_time)
            if remaining > 0 and sound_count % 5 == 0:
                print("    (%.0f seconds remaining...)" % remaining)

    except KeyboardInterrupt:
        print("\n[!] Stopped by user")

    print("")
    print("[OK] Played %d sounds" % sound_count)

print("=" * 50)
