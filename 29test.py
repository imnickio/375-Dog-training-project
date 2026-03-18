import gpiod
import time

CHIP_NAME = 'gpiochip1'
LINE_OFFSET = 14  # This is the standard offset for Physical Pin 29

def test_pin_29():
    try:
        chip = gpiod.Chip(CHIP_NAME)
        line = chip.get_line(LINE_OFFSET)
        line.request(consumer="BypassTest", type=gpiod.LINE_REQ_DIR_OUT)
        
        print(f"Testing Pin 29 (Offset {LINE_OFFSET})...")
        for _ in range(10):
            line.set_value(1)
            time.sleep(0.5)
            line.set_value(0)
            time.sleep(0.5)
        line.release()
    except Exception as e:
        print(f"Pin 29 failed: {e}")

if __name__ == "__main__":
    test_pin_29()
