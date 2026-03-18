import gpiod
import time

# Use the chip number we found earlier
CHIP_NAME = 'gpiochip1'
LINE_OFFSET = 18  # Physical Pin 12

def run_blink():
    try:
        # 1. Open the chip
        chip = gpiod.Chip(CHIP_NAME)
        # 2. Get the line
        line = chip.get_line(LINE_OFFSET)
        
        # 3. Request it as an output
        # (Using the older positional arguments)
        line.request(consumer="BlinkTest", type=gpiod.LINE_REQ_DIR_OUT)

        print(f"Successfully claimed Line {LINE_OFFSET} on {CHIP_NAME}!")
        print("Blinking LED on Physical Pin 12... (Ctrl+C to stop)")

        while True:
            line.set_value(1)
            print("LED: [ ON  ]")
            time.sleep(1)
            
            line.set_value(0)
            print("LED: [ OFF ]")
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'line' in locals():
            line.release()

if __name__ == "__main__":
    run_blink()
