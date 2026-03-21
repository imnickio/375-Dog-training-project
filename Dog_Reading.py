import requests
import base64
import os
import json 

API_KEY = "2DqULRG06WgrWpX6WSwC" 
WORKSPACE = "jenwindows-workspace"
PROJECT = "find-dogs-tuzes-instant"
VERSION = "1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")


        url = "https://detect.roboflow.com/" + WORKSPACE + "/" + PROJECT + "/" + VERSION
        
      
        headers = {
            "Content-Type": "application/json"
        }
        
        
        payload = {
            "api_key": API_KEY,
            "image": img_data,
            "confidence": 40
        }

  
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            if "predictions" in result and len(result["predictions"]) > 0:
                print("SUCCESS: Dog detected!")
                return True
            return False
        else:
            print("Status: " + str(response.status_code) + " - " + response.text)
            return False

    except Exception as e:
        print("Error: " + str(e))
        return False
