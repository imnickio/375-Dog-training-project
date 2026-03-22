import subprocess
import json
import os
import base64
import requests
import time

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    """Forcefully captures an image by clearing system locks first."""
    # 1. Kill any 'zombie' camera processes
    subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
    
    # 2. Clean up old files
    if os.path.exists(filename):
        os.remove(filename)

    try:
        # 3. Use the exact command you said works in the terminal
        # -S 15 gives the camera sensor time to 'warm up' so it doesn't save a 0-byte file
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "-S", "15", filename
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 4. Final check - wait for the SD card to write
        time.sleep(2)
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            return True
    except Exception as e:
        print("System call failed: {}".format(e))
        
    return False

def is_dog_present(*args):
    """The main AI logic."""
    if not capture_image():
        print("!! CAMERA ERROR: The script couldn't save the file. !!")
        return False

    try:
        with open("scan.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"api_key": API_KEY}
        
        response = requests.post(URL, params=params, data=encoded_string, headers=headers, timeout=15)
        
        print("\n--- AI RESPONSE ---")
        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            if not predictions:
                print("Camera is working, but no dog in frame.")
            for p in predictions:
                print("- {} ({:.0%})".format(p['class'], p['confidence']))
                if p['class'] == 'dog' and p['confidence'] > 0.35:
                    return True
        else:
            print("API Error: {}".format(response.text))
            
        return False

    except Exception as e:
        print("Python Error: {}".format(e))
        return False
