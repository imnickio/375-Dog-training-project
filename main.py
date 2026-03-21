import cv2
import time
import motor
import sound
from Dog_Reading import is_dog_present

# Initialize hardware
motor.setup_motors()
camera = cv2.VideoCapture(0)

print("--- Dog Trainer System Active ---")

try:
    while True:
        # 1. Capture Image
        ret, frame = camera.read()
        if not ret:
            continue
        
        temp_img = "current_capture.jpg"
        cv2.imwrite(temp_img, frame)

        # 2. Check AI
        if is_dog_present(temp_img):
            print("Dog detected! Starting reward sequence...")
            
            # 3. Play Sound
            sound.play_audio("goodboy_fixed.wav")
            
            # 4. Spin Motor
            motor.spin_dispenser(1.5)
            
            # 5. Cooldown (Don't overfeed!)
            print("Sequence complete. Waiting 10 seconds...")
            time.sleep(10)
        
        # Check once every second to save API usage
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down safely...")
finally:
    camera.release()
    motor.cleanup()
