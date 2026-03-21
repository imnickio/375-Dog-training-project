import RPi.GPIO as GPIO
import time


PWMA = 18 # Physical Pin 12 - Connected to PWMA
AIN1 = 17 # Physical Pin 11 - Connected to AIN1
AIN2 = 27 # Physical Pin 13 - Connected to AIN2

def setup_motors():
    """Initializes the GPIO pins for the motor driver."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([PWMA, AIN1, AIN2], GPIO.OUT)
    
    GPIO.output(PWMA, GPIO.HIGH)

def spin_dispenser(seconds=1.5):
    """
    Spins the motor in one direction to dispense a treat.
    """
    print(f"Motor: Spinning for {seconds}s...")
    
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    
    time.sleep(seconds)
    
    
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    print("Motor: Stopped.")

def cleanup():
    """Cleans up GPIO pins on exit."""
    GPIO.cleanup()
