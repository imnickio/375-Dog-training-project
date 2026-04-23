import time
import random
import gc
import motor
import Dog_Reading
import sound_handler

# --- CONFIG ---

POSES_TO_TRAIN = ["sit", "lie"] 
WAIT_TIME = 1.0  
SAMPLES = 2   

def wait_for_dog():
    print("System Idle: Waiting for dog...")
    while True:
        current_pose = Dog_Reading.get_dog_pose()
       
        if current_pose in ["sit", "lie", "stand"]:
            print(f"Dog detected ({current_pose})! Starting session...")
            return True
        time.sleep(0.5) 

def train_until_success(target_pose):
    success = False
    attempts = 0
    
    while not success:
        attempts += 1
        audio_file = "sit_fixed.wav" if target_pose == "sit" else "lay_command.wav"
        
        print(f"\n[Attempt {attempts}] Command: {target_pose.upper()}")
        sound_handler.play_audio(audio_file)
        
        
        time.sleep(WAIT_TIME)
        
        print(f"Checking for {target_pose}...")
       
        current_ai_see = Dog_Reading.get_dog_pose()
        
        if current_ai_see == target_pose:
            print(f"MATCH! AI confirmed {target_pose.upper()}.")
            sound_handler.play_audio("goodboy_fixed.wav")
            motor.spin_dispenser(1.5)
            success = True
        else:
            print(f"Saw {current_ai_see}. Repeating...")
            time.sleep(0.5)

def main():
    motor.setup_motors()
    print("\n--- PAO-VLOV ONLINE (V3.0) ---")
    
    try:
        while True:
            wait_for_dog()
            target = random.choice(POSES_TO_TRAIN)
            train_until_success(target)
            
            print("Great job! Resetting for 10 seconds...")
            time.sleep(10)
            gc.collect()
            
    except KeyboardInterrupt:
        motor.cleanup()

if __name__ == "__main__":
    main()
