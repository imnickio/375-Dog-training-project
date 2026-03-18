import gpiod
import time

CHIP_NAME = 'gpiochip1'

def find_working_pin():
    chip = gpiod.Chip(CHIP_NAME)
    # We will test common Orin Nano ranges: 0-20 and 100-120
    test_range = list(range(0, 30)) + list(range(100, 150))
    
    print("Scanning for a valid GPIO line... Watch your LED!")
    
    for offset in test_range:
        try:
            line = chip.get_line(offset)
            line.request(consumer="Finder", type=gpiod.LINE_REQ_DIR_OUT)
            
            print(f"Testing Line: {offset}...", end="\r")
            
            # Blink fast so you can see it
            for _ in range(4):
                line.set_value(1)
                time.sleep(0.1)
                line.set_value(0)
                time.sleep(0.1)
                
            line.release()
        except (ValueError, OSError, PermissionError):
            # This skips 'Invalid Argument' or 'Busy' lines automatically
            continue

    print("\nScan complete. Did any offset make the LED flash?")

if __name__ == "__main__":
    find_working_pin()
