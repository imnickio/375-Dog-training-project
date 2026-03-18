import gpiod
import time

CHIP_NAME = 'gpiochip1'
# These are the most common 'Line' offsets for the Orin Nano header
test_offsets = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

def scan_pins():
    chip = gpiod.Chip(CHIP_NAME)
    print("Starting Pin Scanner... Move your wire across the pins!")
    
    try:
        for offset in test_offsets:
            print(f"Testing Line Offset: {offset}")
            line = chip.get_line(offset)
            try:
                line.request(consumer="Scanner", type=gpiod.LINE_REQ_DIR_OUT)
                for _ in range(3): # Blink 3 times fast
                    line.set_value(1)
                    time.sleep(0.2)
                    line.set_value(0)
                    time.sleep(0.2)
                line.release()
            except:
                print(f"Line {offset} is busy, skipping...")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("Scanner stopped.")

if __name__ == "__main__":
    scan_pins()
