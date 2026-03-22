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
    # Clear memory/files from previous runs
    subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Use a smaller resolution (320x240) to save RAM
        # The AI doesn't need 1080p to see a dog!
        subprocess.run([
            "fswebcam", "-r", "320x240", "--no-banner", "-F", "1", "-S", "10", filename
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        time.sleep(1)
        return os.path.exists(filename)
    except Exception:
        return False

def is_dog_present(*args):
    if not capture_image():
        return False

    try:
        # 1. Open the file and encode it 
        with open("scan.jpg", "rb") as image_file:
            # We encode it and immediately send it so it doesn't sit in a variable
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"api_key": API_KEY}
        
        # 2. Send the request
        response = requests.post(URL, params=params, data=encoded_string, headers=headers, timeout=10)
        
        # 3. Clear the big string from memory immediately
        del encoded_string 

        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            for p in predictions:
                print("- Found: {} ({:.0%})".format(p['class'], p['confidence']))
                if p['class'] == 'dog' and p['confidence'] > 0.35:
                    return True
        return False

    except Exception as e:
        print("Memory/Network Error: {}".format(e))
        return False
