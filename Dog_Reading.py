import os
import json
import base64

API_KEY = "2DqULRG06WgrWpX6WSwC" 
WORKSPACE = "jenwindows-workspace"
PROJECT = "find-dogs-tuzes-instant"
VERSION = "1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        
        url = "https://detect.roboflow.com/" + WORKSPACE + "/" + PROJECT + "/" + VERSION + "?api_key=" + API_KEY
        
        command = "curl -s -X POST '" + url + "' --data-binary @" + image_path
        
 
        response_text = os.popen(command).read()
        
        if not response_text:
            return False

        result = json.loads(response_text)

        if "predictions" in result and len(result["predictions"]) > 0:
            print("CURL SUCCESS: Dog found!")
            return True
        
        return False

    except Exception as e:
        print("System Error: " + str(e))
        return False
