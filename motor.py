import RPi.GPIO as GPIO
import time

PWMA, AIN1, AIN2 = 18, 17, 27 

def setup_motors():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([PWMA, AIN1, AIN2], GPIO.OUT)
    # Ensure motor is OFF during setup
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(PWMA, GPIO.HIGH) 

def spin_dispenser(seconds=1.5):
    print("Motor: Dispensing...")
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    time.sleep(seconds)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)

def cleanup():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.cleanup()

