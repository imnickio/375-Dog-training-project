import cv2
import time
import motor
import sound
from Dog_Reading import is_dog_present

motor.setup_motors()
cap = cv2.VideoCapture(0)

print("System Active on Stretch OS...")

try:
    while True:
        ret, frame = cap.read()
        if ret:
            img = "scan.jpg"
            cv2.imwrite(img, frame)
            
            if is_dog_present(img):
                print("Dog detected!")
                sound.play_audio("goodboy_fixed.wav")
                motor.spin_dispenser(1.5)
                time.sleep(10)
        
        time.sleep(1)
finally:
    cap.release()
    motor.cleanup()
