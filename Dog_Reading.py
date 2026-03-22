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
    """Attempts to capture using sudo and multiple device paths."""
    if os.path.exists(filename):
        try:
            os.remove(filename)
        except:
            pass
            
    # Try video0 first, then video1 as a backup
    for device in ["/dev/video0", "/dev/video1"]:
        if not os.path.exists(device):
            continue
            
        try:
            # We use 'sudo' here because sometimes the 'pi' user lacks video group rights
            subprocess.run([
                "sudo", "fswebcam", "-d", device, "-r", "640x480", 
                "--no-banner", "-F", "1", "-S", "20", filename
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            time.sleep(1.5) # Critical delay for slow SD cards
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                return True
        except Exception:
            continue
    return False

def is_dog_present(*args):
    """Sends Base64 data with the required Content-Type header."""
    if not capture_image():
        print("!! CAMERA ERROR: No image saved to disk !!")
        return False

    try:
        with open("scan.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        params = {"api_key": API_KEY}
        
        response = requests.post(
            URL, 
            params=params, 
            data=encoded_string, 
            headers=headers, 
            timeout=15
        )
        
        print("\n--- AI RESPONSE ---")
        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            if not predictions:
                print("Seeing clearly, but no dog found.")
            for p in predictions:
                print("- {} ({:.0%})".format(p['class'], p['confidence']))
                if p['class'] == 'dog' and p['confidence'] > 0.30:
                    return True
        else:
            print("Server Error: {}".format(response.text))
            
        return False

    except Exception as e:
        print("Python Error: {}".format(e))
        return False
