import os
import json
import base64

API_KEY = "2DqULRG06WgrWpX6WSwC" 
WORKSPACE = "jenwindows-workspace"
PROJECT = "find-dogs-tuzes-instant"
VERSION = "1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        print("Error: scan.jpg not found!")
        return False

    try:
        url = "https://detect.roboflow.com/" + WORKSPACE + "/" + PROJECT + "/" + VERSION + "?api_key=" + API_KEY
        command = "curl -s -X POST '" + url + "' --data-binary @" + image_path
        
        # Run the command
        response_text = os.popen(command).read()
        
        # --- NEW DEBUG LINES ---
        print("RAW RESPONSE FROM AI: " + response_text)
        # -----------------------

        if not response_text:
            print("CURL returned nothing. Check your internet!")
            return False

        result = json.loads(response_text)

        # Check if the server sent an error message instead of a prediction
        if "error" in result:
            print("AI Server Error: " + str(result["error"]))
            return False

        if "predictions" in result and len(result["predictions"]) > 0:
            print("SUCCESS: Dog found!")
            return True
        
        return False

    except Exception as e:
        print("Python Error: " + str(e))
        return False
