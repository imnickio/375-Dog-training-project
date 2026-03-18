import Jetson.GPIO as GPIO
import time

# Pin Definitions
led_pin = 7 # The physical pin where the LED is connected

# Pin Setup
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) # Set pin as an output and start LOW (off)

print("Press CTRL+C to stop the blinking")

# Blink the LED
try:
    while True:
        GPIO.output(led_pin, GPIO.HIGH) # Turn LED on
        time.sleep(0.5) # Wait for 500ms
        GPIO.output(led_pin, GPIO.LOW) # Turn LED off
        time.sleep(0.5) # Wait for 500ms
except KeyboardInterrupt:
    print("Exiting gracefully")
    # Cleanup all GPIOs to ensure a clean exit
    GPIO.cleanup()
