import Jetson.GPIO as GPIO
import time
import sys
# Pin Configuration
LED_PIN = 7
# LED Anode (+) -> Pin 15 (via 220Ω resistor)
# LED Cathode (-) -> GND (Pin 6, 9, 14, 20, 25, 30, 34, or 39)
# Hardware Setup
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
# Blink LED continuously
while True:
  GPIO.output(LED_PIN, GPIO.HIGH)
  time.sleep(0.5)
  GPIO.output(LED_PIN, GPIO.LOW)
  time.sleep(0.5)
