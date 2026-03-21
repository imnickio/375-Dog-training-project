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
        

        payload = {
            "api_key": API_KEY,
            "image": img_data,
            "confidence": 40
        }


        headers = {"Content-Type": "application/json"}
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        
       
        print("Server Status: " + str(response.status_code))
        
        if response.status_code == 200:
            result = response.json()
            if "predictions" in result and len(result["predictions"]) > 0:
                print("SUCCESS: Dog spotted!")
                return True
        else:
            print("Server said: " + response.text)
            
        return False

    except Exception as e:
        print("Error: " + str(e))
        return False
