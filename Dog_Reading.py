import requests
import base64
import os


API_KEY = "2DqULRG06WgrWpX6WSwC" 
PROJECT_ID = "find-dogs-tuzes-instant/1" 

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

    
        url = "https://detect.roboflow.com/" + PROJECT_ID
        
        params = {
            "api_key": API_KEY,
            "confidence": "40"
        }

       
        response = requests.post(url, params=params, data=img_data)
        
        print("Inference Status: " + str(response.status_code))
        
        if response.status_code == 200:
            result = response.json()
            if "predictions" in result and len(result["predictions"]) > 0:
                print("INFERENCE SUCCESS: Dog spotted!")
                return True
        else:
            print("Response: " + response.text)
            
        return False

    except Exception as e:
        print("Inference Error: " + str(e))
        return False
