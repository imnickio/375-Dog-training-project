import requests
import time
import subprocess
import os

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    """Uses fswebcam to grab a frame and then IMMEDIATELY release the camera."""
    try:
        # We use -F 1 to take just one frame and exit quickly
        subprocess.run(["fswebcam", "-r", "640x480", "--no-banner", "-F", "1", filename], check=True)
        return True
    except Exception as e:
        print("Camera is still busy! Try: sudo fuser -k /dev/video0")
        return False

def is_dog_present(*args):
    if not capture_image():
        return False

    params = {"api_key": API_KEY}
    
    try:
        # Using 'with' ensures the file is closed immediately after the request
        with open("scan.jpg", "rb") as image_file:
            files = {"file": image_file}
            response = requests.post(URL, params=params, files=files, timeout=10)
            
            if response.status_code == 200:
                predictions = response.json().get("predictions", [])
                for p in predictions:
                    if p['class'] == 'dog' and p['confidence'] > 0.4:
                        print("DOG DETECTED! Confidence: {}".format(p['confidence']))
                        return True
                print("No dog found.")
            else:
                print("API Error: {} - {}".format(response.status_code, response.text))
    except Exception as e:
        print("Network/File Error: {}".format(e))
        
    return False
