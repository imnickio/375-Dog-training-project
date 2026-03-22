import subprocess
import json
import os
import time

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"

def is_dog_present(*args):
    """Uses the reliable 'curl' method, compatible with Python 3.5."""
    
    # 1. Take the photo using fswebcam
    try:
        # We skip 2 frames (-S 2) to let the camera adjust its brightness
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-S", "2", "scan.jpg"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        # If 'Device Busy', try to kick the ghost processes
        subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
        return False

    # 2. Setup the Curl Command
    url = "https://detect.roboflow.com/{}?api_key={}".format(MODEL_ID, API_KEY)
    curl_command = [
        "curl", "-s", "-X", "POST", url, "--data-binary", "@scan.jpg"
    ]
    
    try:
        # For Python 3.5, we use stdout=subprocess.PIPE instead of capture_output
        process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Convert bytes to string and then to JSON
        response_data = json.loads(stdout.decode('utf-8'))
        
        predictions = response_data.get("predictions", [])
        for p in predictions:
            # Check for 'dog' (or 'microwave' for testing!)
            if p['class'] == 'dog' and p['confidence'] > 0.4:
                print("DOG SPOTTED! Confidence: {:.2f}".format(p['confidence']))
                return True
        
        print("No dog found in kitchen.")
        return False

    except Exception as e:
        print("AI Connection Error: {}".format(e))
        return False
