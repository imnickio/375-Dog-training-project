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
    """Captures a frame and waits for the file to save."""
    if os.path.exists(filename):
        os.remove(filename)
    try:
        # -S 15: Skip 15 frames to ensure the image isn't pitch black
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "-S", "15", filename
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Give the Pi a moment to finish writing the file to the SD card
        time.sleep(1) 
        return os.path.exists(filename)
    except Exception:
        return False

def is_dog_present(*args):
    """Sends Base64 data with the required Content-Type header."""
    if not capture_image():
        print("Camera failed to save image.")
        return False

    try:
        # 1. Encode to Base64
        with open("scan.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # 2. Set Headers and Params
        # This header tells the server: "I am sending you a long string of data"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"api_key": API_KEY}
        
        # 3. Post the request
        response = requests.post(
            URL, 
            params=params, 
            data=encoded_string, 
            headers=headers, 
            timeout=15
        )
        
        print("\n--- RAW SERVER RESPONSE ---")
        print(response.text)
        print("---------------------------\n")

        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            for p in predictions:
                if p['class'] == 'dog' and p['confidence'] > 0.30:
                    print(">>> DOG DETECTED! ({:.1%}) <<<".format(p['confidence']))
                    return True
            print("No dog found.")
        else:
            print("Server Error: {} - {}".format(response.status_code, response.text))
            
        return False

    except Exception as e:
        print("Script Error: {}".format(e))
        return False
