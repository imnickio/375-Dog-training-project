import requests
import time
import subprocess
import os

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    """Uses the low-level v4l2-ctl to grab a frame."""
    try:
        # This command forces a capture without trying to 'negotiate' with the driver
        subprocess.run([
            "v4l2-ctl", "--device=/dev/video0", 
            "--set-fmt-video=width=640,height=480,pixelformat=MJPG", 
            "--stream-mmap", "--stream-count=1", 
            "--stream-to=" + filename
        ], check=True)
        return True
    except Exception as e:
        # If even that fails, your Pi might not be giving the camera enough POWER.
        print("Hardware Error: Is your power supply at least 2.5A?")
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
