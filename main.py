import cv2
import time
import motor
import sound
from Dog_Reading import is_dog_present

print("--- Initializing Hardware ---")
motor.setup_motors()

print("--- Hardware Ready ---")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("ERROR: Could not open camera!")

print("--- Starting Main Loop: Watching for Dog ---")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera failed to grab frame...")
            time.sleep(2)
            continue
        
        # Take a picture and check it
        img = "scan.jpg"
        cv2.imwrite(img, frame)
        print("Saved image size: " + str(os.path.getsize(img)) + " bytes")
        print("Checking AI...")
        if is_dog_present(img):
            print("MATCH! Dog found.")
            sound.play_audio("goodboy_fixed.wav")
            motor.spin_dispenser(1.5)
            print("Waiting 10s cooldown...")
            time.sleep(10)
        else:
            print("No dog seen. Sleeping 1s...")
            time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping system...")
finally:
    cap.release()
    motor.cleanup()
