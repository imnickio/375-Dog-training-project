import os
import time
import motor
import sound
from Dog_Reading import is_dog_present

print("--- Initializing Hardware ---")
motor.setup_motors()
print("--- Hardware Ready ---")
print("--- Starting Main Loop: Watching for Dog ---")

try:
    while True:
        # We no longer pass 'img' because Dog_Reading handles its own capture
        print("Checking AI...")
        
        if is_dog_present():
            print("MATCH! Dog found.")
            sound.play_audio("goodboy_fixed.wav")
            motor.spin_dispenser(1.5)
            print("Waiting 10s cooldown...")
            time.sleep(10)
        else:
            # Increased sleep to 2s to give the CPU/RAM a breather
            print("No dog seen. Sleeping 2s...")
            time.sleep(2)

except KeyboardInterrupt:
    print("\nStopping system...")
finally:
    motor.cleanup()
