import os
import time

# Pin 15 on the Orin Nano header corresponds to Linux GPIO index 440
# (Note: This index can vary, but 440 is the standard for Pin 15)
GPIO_PIN = "440" 
GPIO_PATH = f"/sys/class/gpio/gpio{GPIO_PIN}"

def setup_pin():
    # 1. Export the pin (tell Linux we want to use it)
    if not os.path.exists(GPIO_PATH):
        try:
            with open("/sys/class/gpio/export", "w") as f:
                f.write(GPIO_PIN)
        except Exception as e:
            print(f"Export failed: {e}. Try running with sudo.")
            return False

    # 2. Set direction to 'out'
    time.sleep(0.1) # Give Linux a millisecond to create the folder
    with open(f"{GPIO_PATH}/direction", "w") as f:
        f.write("out")
    return True

def set_led(state):
    # Write '1' for ON, '0' for OFF
    with open(f"{GPIO_PATH}/value", "w") as f:
        f.write(str(state))

if __name__ == "__main__":
    if setup_pin():
        print("Bypassing all libraries! Blinking Pin 15...")
        try:
            while True:
                set_led(1)
                time.sleep(0.5)
                set_led(0)
                time.sleep(0.5)
        except KeyboardInterrupt:
            # Cleanup
            with open("/sys/class/gpio/unexport", "w") as f:
                f.write(GPIO_PIN)
