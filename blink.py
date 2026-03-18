import gpiod
import time

# CONFIGURATION FOR PHYSICAL PIN 12
CHIP_NAME = 'gpiochip1'
LINE_OFFSET = 18  # This is the offset for Physical Pin 12

def run_blink():
    try:
        # 1. Open the GPIO chip
        chip = gpiod.Chip(CHIP_NAME)
        # 2. Select Line 18
        line = chip.get_line(LINE_OFFSET)
        
        # 3. FORCE the pin to become an OUTPUT
        # We use consumer='BlinkTest' so the system knows who is using it
        config = gpiod.line_request()
        config.consumer = "BlinkTest"
        config.request_type = gpiod.line_request.DIRECTION_OUTPUT
        line.request(config)

        print(f"Successfully claimed Line {LINE_OFFSET} on {CHIP_NAME}.")
        print("Blinking LED on Physical Pin 12... (Press Ctrl+C to stop)")

        while True:
            line.set_value(1)  # Turn ON
            print("LED: [ ON  ]")
            time.sleep(1)
            
            line.set_value(0)  # Turn OFF
            print("LED: [ OFF ]")
            time.sleep(1)

    except PermissionError:
        print("Error: Permission Denied. Try running with 'sudo'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'line' in locals():
            line.release()
            print("\nPin released. Hardware reset to default.")

if __name__ == "__main__":
    run_blink()
