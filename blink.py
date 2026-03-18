import gpiod
import time

CHIP_PATH = '/dev/gpiochip1'
LINE_OFFSET = 18  # Physical Pin 12

def run_blink():
    # Use 'with' so it automatically cleans up even if it crashes
    try:
        with gpiod.request_lines(
            CHIP_PATH,
            consumer="BlinkTest",
            config={
                LINE_OFFSET: gpiod.LineSettings(
                    direction=gpiod.line.Direction.OUTPUT,
                    output_value=gpiod.line.Value.LOW
                )
            },
        ) as request:
            print(f"Claimed Line {LINE_OFFSET} on {CHIP_PATH}!")
            print("Blinking LED on Physical Pin 12... (Ctrl+C to stop)")
            
            while True:
                request.set_value(LINE_OFFSET, gpiod.line.Value.ACTIVE)
                print("LED: [ ON  ]")
                time.sleep(1)
                
                request.set_value(LINE_OFFSET, gpiod.line.Value.INACTIVE)
                print("LED: [ OFF ]")
                time.sleep(1)

    except PermissionError:
        print("Error: Permission Denied. Run with 'sudo python3 test_blink.py'")
    except Exception as e:
        print(f"Error: {e}")
        print("\nIf it says 'Invalid argument', run 'gpioinfo' to verify Line 18 is correct.")

if __name__ == "__main__":
    run_blink()
    
