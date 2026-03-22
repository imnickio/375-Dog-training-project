import subprocess
import json
import os
import time

# --- CONFIGURATION ---
# Using the exact API key and Public model that worked for you
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"

def is_dog_present(*args):
    """Uses the reliable 'curl' method to check for a dog."""
    
    # 1. Take the photo using fswebcam (The most 'stable' way on Pi)
    # We use -F 1 to take one frame and immediately RELEASE the camera.
    try:
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "scan.jpg"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        # If it's busy, we try to force-kill any ghost processes
        subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
        return False

    # 2. Use the 'curl' command that you confirmed worked earlier
    # This sends the image to Roboflow and gets the answer back as text
    curl_command = [
        "curl", "-s", "-X", "POST",
        "https://detect.roboflow.com/{}?api_key={}".format(MODEL_ID, API_KEY),
        "--data-binary", "@scan.jpg"
    ]
    
    try:
        result = subprocess.run(curl_command, capture_output=True, text=True)
        response_data = json.loads(result.stdout)
        
        predictions = response_data.get("predictions", [])
        for p in predictions:
            # Check for 'dog' with at least 40% confidence
            if p['class'] == 'dog' and p['confidence'] > 0.4:
                print("DOG SPOTTED! Confidence: {:.2f}".format(p['confidence']))
                return True
        
        print("No dog found in kitchen.")
        return False

    except Exception as e:
        print("AI Connection Error: {}".format(e))
        return False
