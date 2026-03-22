import subprocess
import json
import os
import base64
import requests
import time
import gc  # Garbage Collector to reclaim RAM

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    """Captures a higher-res snap now that memory is stable."""
    # Force kill any lingering camera locks
    subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
    
    if os.path.exists(filename):
        os.remove(filename)

    try:
        # Back to 640x480 for better detail
        # -S 30: Gives the camera ~1.5 seconds to adjust brightness
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "-S", "30", filename
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        return os.path.exists(filename)
    except Exception:
        return False

def is_dog_present():
    if not capture_image():
        return False

    try:
        # 1. Encode image and immediately prepare headers
        with open("scan.jpg", "rb") as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"api_key": API_KEY}
        
        # 2. Make the request
        response = requests.post(URL, params=params, data=img_data, headers=headers, timeout=10)
        
        # 3. CRITICAL: Wipe the image data from RAM immediately
        img_data = None
        gc.collect() 

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
