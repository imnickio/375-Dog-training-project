import requests
import base64
import os


API_KEY = "AU8JxB1DTPRTyxA9qcqL"
PROJECT_ID = "find-dogs-tuzes-instant" 
VERSION = "1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
     
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

    
        url = "https://detect.roboflow.com/" + PROJECT_ID + "/" + VERSION
        
        params = {
            "api_key": API_KEY,
            "confidence": 40 
        }

        
        response = requests.post(url, params=params, data=img_data)
        
        
        if response.status_code != 200:
            print("Status: " + str(response.status_code) + " - " + response.text)
            return False

        result = response.json()

       
        if "predictions" in result and len(result["predictions"]) > 0:
            
            found_class = result["predictions"][0]["class"]
            print("Success! AI saw: " + str(found_class))
            return True
        
        return False

    except Exception as e:
        print("Error: " + str(e))
        return False
