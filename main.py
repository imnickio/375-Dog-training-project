import time
import random
import gc
import motor
import Dog_Reading
import sound_handler

# --- CONFIG ---
POSES_TO_TRAIN = ["sit", "lay"]
WAIT_TIME = 1.5  
SAMPLES = 2      

def wait_for_dog():
    """Only triggers if it sees an actual dog pose, NOT 'indoor' or 'nothing'"""
    print("System Idle: Waiting for dog...")
    while True:
        current_pose = Dog_Reading.get_dog_pose()
        
     
        if current_pose in ["sit", "lay", "stand"]:
            print(f"Dog detected ({current_pose})! Starting session...")
            return True
        
        time.sleep(1)

def train_until_success(target_pose):
    """The 'Stubborn' Loop: Repeats command until dog obeys"""
    success = False
    attempts = 0
    
    while not success:
        attempts += 1
        audio_file = "sit_fixed.wav" if target_pose == "sit" else "lay_command.wav"
        
        print(f"\n[Attempt {attempts}] Command: {target_pose.upper()}")
        sound_handler.play_audio(audio_file)
        
       
        time.sleep(WAIT_TIME)
        
  
        print(f"Checking for {target_pose}...")
        detections = [Dog_Reading.get_dog_pose() for _ in range(SAMPLES)]
        
        if target_pose in detections:
            print(f"SUCCESS! Dog is in {target_pose} pose.")
            sound_handler.play_audio("goodboy_fixed.wav")
            motor.spin_dispenser(1.5)
            success = True
        else:
            print(f"Not quite. AI saw: {detections}. Repeating command...")
           
            time.sleep(1)

def main():
    motor.setup_motors()
    print("\n--- PAO-VLOV ONLINE ---")
    
    try:
        while True:
            
            wait_for_dog()
            
            target = random.choice(POSES_TO_TRAIN)
            
        
            train_until_success(target)
            
            print("Round complete! Resetting for 10 seconds...")
            time.sleep(10)
            gc.collect()
            
    except KeyboardInterrupt:
        motor.cleanup()

if __name__ == "__main__":
    main()
