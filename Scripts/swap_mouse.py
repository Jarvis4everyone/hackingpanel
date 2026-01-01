# -*- coding: utf-8 -*-
"""
Swap Mouse Buttons
Swaps left and right mouse buttons
Run again to swap back
"""
import ctypes
import os

# Action: swap, normal, toggle
ACTION = os.environ.get("MOUSE_ACTION", "toggle").lower()

print("=" * 50)
print("   SWAP MOUSE BUTTONS")
print("=" * 50)
print(f"   Action: {ACTION}")
print("=" * 50)

user32 = ctypes.windll.user32

# SystemParametersInfo constants
SPI_SETMOUSEBUTTONSWAP = 0x0021
SPI_GETMOUSEBUTTONSWAP = 0x0021  # Actually use GetSystemMetrics for this

# GetSystemMetrics constant
SM_SWAPBUTTON = 23

def is_swapped():
    """Check if mouse buttons are currently swapped."""
    return bool(user32.GetSystemMetrics(SM_SWAPBUTTON))

def swap_buttons(swap):
    """Swap or unswap mouse buttons."""
    # SwapMouseButton: TRUE to swap, FALSE to restore
    result = user32.SwapMouseButton(swap)
    return True

try:
    current_state = is_swapped()
    print(f"[*] Current state: {'Swapped' if current_state else 'Normal'}")
    
    if ACTION == "swap":
        swap_buttons(True)
        new_state = True
    elif ACTION == "normal":
        swap_buttons(False)
        new_state = False
    else:  # toggle
        swap_buttons(not current_state)
        new_state = not current_state
    
    print(f"[*] New state: {'Swapped' if new_state else 'Normal'}")
    
    if new_state:
        print("\n[OK] Mouse buttons SWAPPED!")
        print("    Left click = Right click")
        print("    Right click = Left click")
    else:
        print("\n[OK] Mouse buttons NORMAL!")
        print("    Left click = Left click")
        print("    Right click = Right click")

except Exception as e:
    print(f"[ERROR] {e}")

print("\n" + "=" * 50)
print("Tip: Run again or set MOUSE_ACTION=normal to restore")
print("=" * 50)

