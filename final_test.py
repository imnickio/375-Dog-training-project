import subprocess
import os
import base64
import requests
import time
import gc
import motor # Ensure your motor.py is in the same folder

# --- CONFIGURATION ---
API_KEY = "NPwSzzX6IxxvAsFWXWm1"
MODEL_ID = "dog-pose-ahfet/1"
URL = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"

def capture_image(filename="scan.jpg"):
    """Uses your proven USB webcam logic"""
    # Force kill any hung camera processes
    subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
    
    if os.path.exists(filename):
        os.remove(filename)

    try:
        # -S 30 skips 30 frames to allow the camera to auto-adjust brightness
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "-S", "30", filename
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return os.path.exists(filename)
    except Exception as e:
        print(f"! Camera Error: {e}")
        return False

def check_ai():
    """Captures a photo and asks the Classification AI for the pose"""
    if not capture_image():
        print("! Failed to grab frame from USB Camera")
        return None

    try:
        with open("scan.jpg", "rb") as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(URL, data=img_data, headers=headers, timeout=10)
        
        # Memory Cleanup
        img_data = None
        gc.collect()

        if response.status_code == 200:
            res = response.json()
            prediction = res.get("top")
            confidence = res.get("predictions", {}).get(prediction, {}).get("confidence", 0)
            return prediction, confidence
        else:
            print(f"! Roboflow Error: {response.status_code}")
            return None, 0

    except Exception as e:
        print(f"! System Error: {e}")
        return None, 0

def run_test():
    print("--- STARTING HARDWARE + AI TEST ---")
    motor.setup()
    
    try:
        while True:
            print("\n[STEP 1] Snapping photo...")
            pose, conf = check_ai()
            
            if pose:
                print(f"[STEP 2] AI Result: {pose.upper()} ({conf:.1%})")
                
                # Check for Sit or Lay
                if pose in ["sit", "lay"] and conf > 0.60:
                    print(f"[STEP 3] SUCCESS! Dispensing for {pose}...")
                    motor.spin_dispenser(1.5)
                    print("Waiting 5 seconds for reset...")
                    time.sleep(5)
                else:
                    print("[STEP 3] No action (Pose was 'nothing' or confidence too low)")
            
            print("--- Ready for next scan in 2 seconds ---")
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopping test...")
        motor.cleanup()

if __name__ == "__main__":
    run_test()
