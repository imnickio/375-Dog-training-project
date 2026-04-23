import time
import gc
import motor
import Dog_Reading
import sound_handler

# --- CONFIG ---
POSES_TO_TRAIN = ["sit", "lie"] 
WAIT_TIME = 1.0  
SAMPLES = 2    

def wait_for_dog():
    print("\nSystem Idle: Waiting for dog to enter frame...")
    while True:
        current_pose = Dog_Reading.get_dog_pose()
        if current_pose in ["sit", "lie", "stand"]:
            print(f"Dog detected! Pose: {current_pose.upper()}. Starting session...")
            return True
        time.sleep(0.5)

def train_until_success(target_pose):
    success = False
    attempts = 0
    
    while not success:
        attempts += 1
        audio_file = "sit_fixed.wav" if target_pose == "sit" else "lay_command.wav"
        
        print(f"\n[Attempt {attempts}] Goal: {target_pose.upper()}")
        sound_handler.play_audio(audio_file)
        
 
        time.sleep(WAIT_TIME)
        
        print(f"Checking for {target_pose}...")

        detections = [Dog_Reading.get_dog_pose() for _ in range(SAMPLES)]
        

        if target_pose in detections:
            print(f"MATCH! AI confirmed {target_pose.upper()} in {detections}.")
            sound_handler.play_audio("goodboy_fixed.wav")
            motor.spin_dispenser(1.5)
            success = True
        else:
            print(f"Not yet. AI saw {detections}. Repeating...")
            time.sleep(0.5)

def main():
    motor.setup_motors()
    print("\n" + "="*30)
    print("PAO-VLOV ONLINE: ALTERNATING MODE")
    print("="*30)
    

    current_index = 0
    
    try:
        while True:
         
            wait_for_dog()
            

            target = POSES_TO_TRAIN[current_index]
            
          
            train_until_success(target)
            
        
            current_index = 1 - current_index
            
            print(f"\nRound complete! Next goal will be: {POSES_TO_TRAIN[current_index].upper()}")
            print("Resting for 10 seconds...")
            time.sleep(10)
            gc.collect()
            
    except KeyboardInterrupt:
        print("\nShutting down Pao-vlov...")
        motor.cleanup()

if __name__ == "__main__":
    main()
