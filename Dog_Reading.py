import base64
import requests
import time
import os
import subprocess

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    """Uses fswebcam to bypass pygame's ioctl format errors."""
    try:
        subprocess.run(["fswebcam", "-r", "640x480", "--no-banner", "-S", "2", filename], check=True)
        return True
    except Exception as e:
        print("Hardware Camera Error: {}".format(e))
        return False

def is_dog_present(*args):
    if not capture_image():
        return False

    # The 'files' dictionary automatically sets the Content-Type header to multipart/form-data
    with open("scan.jpg", "rb") as image_file:
        files = {"file": image_file}
        params = {"api_key": API_KEY}
        
        try:
            # We use 'files=' instead of 'data=' to fix the 400 error
            response = requests.post(URL, params=params, files=files, timeout=10)
            
            if response.status_code == 200:
                predictions = response.json().get("predictions", [])
                for p in predictions:
                    if p['class'] == 'dog' and p['confidence'] > 0.4:
                        print("DOG DETECTED!")
                        return True
                print("No dog found.")
            else:
                print("API Error: {} - {}".format(response.status_code, response.text))
        except Exception as e:
            print("Network Error: {}".format(e))
            
    return False
