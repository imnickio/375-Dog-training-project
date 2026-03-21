import requests
import base64
import os

# Use the PRIVATE key here
API_KEY = "2DqULRG06WgrWpX6WSwC" 
PROJECT_ID = "find-dogs-tuzes-instant" 
VERSION = "1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        with open(image_path, "rb") as image_file:
            
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

        
        url = "https://detect.roboflow.com/" + PROJECT_ID + "/" + VERSION + "?api_key=" + API_KEY
        

        response = requests.post(url, data=img_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        if response.status_code != 200:
            print("Server said (" + str(response.status_code) + "): " + response.text)
            return False

        result = response.json()
        if "predictions" in result and len(result["predictions"]) > 0:
            print("SUCCESS! Dog spotted.")
            return True
        
        return False

    except Exception as e:
        print("Pi Error: " + str(e))
        return False
