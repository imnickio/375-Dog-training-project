import RPi.GPIO as GPIO
import time

# Pin setup (BCM numbering)
PWMA = 18 # Physical Pin 12
AIN1 = 17 # Physical Pin 11
AIN2 = 27 # Physical Pin 13

GPIO.setmode(GPIO.BCM)
GPIO.setup([PWMA, AIN1, AIN2], GPIO.OUT)

def spin_motor(duration):
    print("Dispensing Treat...")
    # Set Direction
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    # Set Speed (On)
    GPIO.output(PWMA, GPIO.HIGH)
    
    time.sleep(duration)
    
    # Stop
    GPIO.output(PWMA, GPIO.LOW)
    print("Done!")

try:
    spin_motor(1.5)
finally:
    GPIO.cleanup()
