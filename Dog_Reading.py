import subprocess
import json
import os
import time

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"

def is_dog_present(*args):
    """Captures an image and prints ALL detected objects for debugging."""
    
    # 1. Capture the image
    try:
        # -S 3: Skip 3 frames to give the camera more time to focus/brighten
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-S", "3", "scan.jpg"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("Camera Hardware Busy!")
        return False

    # 2. Run the AI check
    url = "https://detect.roboflow.com/{}?api_key={}".format(MODEL_ID, API_KEY)
    curl_command = ["curl", "-s", "-X", "POST", url, "--data-binary", "@scan.jpg"]
    
    try:
        process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        response_data = json.loads(stdout.decode('utf-8'))
        
        predictions = response_data.get("predictions", [])
        
        # --- DEBUG SECTION: SEE WHAT THE AI SEES ---
        if not predictions:
            print("AI Result: Screen is blank or nothing recognized.")
        else:
            print("--- AI IS SEEING: ---")
            for p in predictions:
                print("- {} ({:.1%})".format(p['class'], p['confidence']))
        # -------------------------------------------

        for p in predictions:
            # The Goal: Look for the dog
            if p['class'] == 'dog' and p['confidence'] > 0.35:
                print(">>> SUCCESS: TARGET DOG IDENTIFIED! <<<")
                return True
        
        return False

    except Exception as e:
        print("AI Connection Error: {}".format(e))
        return False
