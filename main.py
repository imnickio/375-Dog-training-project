import time
import random
import gc
import motor
import Dog_Reading
import sound_handler  


POSES_TO_TRAIN = ["sit", "lay"]
WAIT_TIME = 4 
SAMPLES = 3   

def wait_for_dog():
    """Loops until the AI sees something that isn't 'indoor' or 'nothing'"""
    print("System Idle: Waiting for dog to enter frame...")
    while True:
        current_pose = Dog_Reading.get_dog_pose()
        
        # If AI sees sit, lay, stand, etc. (and NOT indoor/nothing)
        if current_pose not in ["indoor", "nothing", None]:
            print(f"Dog detected! Pose: {current_pose}. Starting training...")
            return True
        
        time.sleep(2) # Check every 2 seconds to save CPU/Battery

def run_training_round():
    # 1. Wait until a dog is actually there
    wait_for_dog()

    # 2. Randomly pick a command
    target_pose = random.choice(POSES_TO_TRAIN)
    audio_file = "sit_fixed.wav" if target_pose == "sit" else "lay_command.wav"
    
    # 3. Use the imported handler
    sound_handler.play_audio(audio_file)
    
    print(f"Command given: {target_pose.upper()}. Waiting {WAIT_TIME}s...")
    time.sleep(WAIT_TIME)
    
    # 4. Verify with AI
    detections = []
    for _ in range(SAMPLES):
        detections.append(Dog_Reading.get_dog_pose())
        time.sleep(0.3)
    
    # 5. Success Check
    if detections.count(target_pose) >= 2:
        print(f"MATCH! Dog performed {target_pose.upper()}.")
        sound_handler.play_audio("goodboy_fixed.wav")
        motor.spin_dispenser(1.5)
        return True
    else:
        print(f"FAILED. AI saw: {detections}")
        return False

def main():
    motor.setup_motors()
    print("\n---PAOVLOV ONLINE ---")
    
    try:
        while True:
            run_training_round()
            print("Round complete. Resetting...")
            time.sleep(5)
            gc.collect()
            
    except KeyboardInterrupt:
        motor.cleanup()

if __name__ == "__main__":
    main()
