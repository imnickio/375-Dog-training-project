import subprocess
import json
import os
import time

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"

def is_dog_present(*args):
    """Captures an image and prints the RAW server response for troubleshooting."""
    
    # 1. Capture the image
    try:
        # We use -F 1 for a quick snap to avoid 'Device Busy'
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "scan.jpg"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("!! Camera Hardware Error (Busy) !!")
        return False

    # 2. Prepare the Curl Command
    url = "https://detect.roboflow.com/{}?api_key={}".format(MODEL_ID, API_KEY)
    curl_command = ["curl", "-s", "-X", "POST", url, "--data-binary", "@scan.jpg"]
    
    try:
        # Run the curl and catch the output
        process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        # Decode the raw text
        raw_response = stdout.decode('utf-8')
        
        # --- TROUBLESHOOTING: PRINT EVERYTHING ---
        print("\n--- RAW SERVER RESPONSE ---")
        print(raw_response)
        print("---------------------------\n")

        # Parse the JSON
        response_data = json.loads(raw_response)
        
        # Check for API-level errors (like 'Invalid Key')
        if "error" in response_data:
            print("API Error Message: {}".format(response_data["error"]))
            return False

        predictions = response_data.get("predictions", [])
        
        for p in predictions:
            # Check for 'dog'
            if p['class'] == 'dog' and p['confidence'] > 0.35:
                print(">>> DOG DETECTED ({:.1%}) <<<".format(p['confidence']))
                return True
        
        return False

    except Exception as e:
        print("Script Error: {}".format(e))
        return False
