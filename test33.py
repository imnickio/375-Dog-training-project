import gpiod
import time

# After enabling PWM in Jetson-IO, Pin 33 is usually 48 or 49
CHIP_NAME = 'gpiochip1'
LINE_OFFSET = 48 

def test_v1_style():
    try:
        # 1. Open the chip
        chip = gpiod.Chip(CHIP_NAME)
        # 2. Get the specific line
        line = chip.get_line(LINE_OFFSET)
        
        # 3. Request it as an output (Version 1.x syntax)
        line.request(consumer="DogTrainer", type=gpiod.LINE_REQ_DIR_OUT)

        print(f"Successfully claimed Line {LINE_OFFSET} on {CHIP_NAME}!")
        print("Blinking Pin 33... (Ctrl+C to stop)")

        while True:
            line.set_value(1)
            print("LED/Motor: [ ON  ]")
            time.sleep(1)
            
            line.set_value(0)
            print("LED/Motor: [ OFF ]")
            time.sleep(1)

    except Exception as e:
        print(f"Error on Line {LINE_OFFSET}: {e}")
        print("If it says 'Invalid Argument', change LINE_OFFSET to 49.")
    finally:
        if 'line' in locals():
            line.release()

if __name__ == "__main__":
    test_v1_style()
