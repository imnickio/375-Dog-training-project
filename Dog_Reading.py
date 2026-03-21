import requests
import base64
import os


API_KEY = "rf_8O04kCCci9YNMgspAnO42LIxOvq2"
PROJECT_ID = "find-dogs-tuzes-instant" 
VERSION = "1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

        url = "https://detect.roboflow.com/" + PROJECT_ID + "/" + VERSION
        
        
        headers = {
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        }
        
       
        payload = {
            "image": img_data,
            "confidence": 40
        }

        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 401:
            print("401 ERROR: The API Key is being rejected. Check for typos!")
            return False
            
        if response.status_code != 200:
            print("Status: " + str(response.status_code) + " - " + response.text)
            return False

        result = response.json()
        if "predictions" in result and len(result["predictions"]) > 0:
            print("AI detected: " + result["predictions"][0]["class"])
            return True
        
        return False

    except Exception as e:
        print("Logic Error: " + str(e))
        return False
