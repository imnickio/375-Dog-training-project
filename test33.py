import gpiod
import time

CHIP = '/dev/gpiochip1'
# After enabling PWM in Jetson-IO, Pin 33 is usually 48. 
# If 48 fails, try 49.
LINE_OFFSET = 48 

def test_after_reboot():
    try:
        with gpiod.request_lines(
            CHIP,
            consumer="DogTrainer",
            config={LINE_OFFSET: gpiod.LineSettings(
                direction=gpiod.line.Direction.OUTPUT
            )}
        ) as request:
            print(f"Success! Pin 33 (Line {LINE_OFFSET}) is ACTIVE.")
            for i in range(5):
                print(f"Blink {i+1}...")
                request.set_value(LINE_OFFSET, gpiod.line.Value.ACTIVE)
                time.sleep(1)
                request.set_value(LINE_OFFSET, gpiod.line.Value.INACTIVE)
                time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_after_reboot()
