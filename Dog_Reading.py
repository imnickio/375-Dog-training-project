import subprocess
import json
import os
import base64
import requests

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    """Captures a single frame using fswebcam."""
    try:
        # -F 1: grab 1 frame. -S 10: skip 10 frames to allow light adjustment
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "-S", "10", filename
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return os.path.exists(filename)
    except Exception:
        return False

def is_dog_present(*args):
    """Encodes image to Base64 and sends to Roboflow."""
    if not capture_image():
        print("Camera capture failed.")
        return False

    try:
        # 1. Convert the image to a Base64 string
        with open("scan.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # 2. Setup the Request
        params = {"api_key": API_KEY}
        
        # 3. Send as DATA (not files) to satisfy the 'Invalid base64' error
        response = requests.post(URL, params=params, data=encoded_string, timeout=15)
        
        print("\n--- RAW SERVER RESPONSE ---")
        print(response.text)
        print("---------------------------\n")

        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            for p in predictions:
                if p['class'] == 'dog' and p['confidence'] > 0.35:
                    print("DOG DETECTED!")
                    return True
            print("No dog found.")
        else:
            print("Server returned error: {}".format(response.status_code))
            
        return False

    except Exception as e:
        print("Error: {}".format(e))
        return False
