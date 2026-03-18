import Jetson.GPIO as GPIO
import time

GPIO.setinfo(GPIO.JETSON_ORIN_NANO)
# Use Physical Pin Numbering
GPIO.setmode(GPIO.BOARD)

LED_PIN = 7

try:
    GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    print("Blinking LED on Pin 15... Press Ctrl+C to stop.")
    
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping...")
finally:
    # This resets the pins so they are safe for the next run
    GPIO.cleanup()
