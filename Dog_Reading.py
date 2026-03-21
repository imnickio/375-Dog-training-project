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

        
        url = "https://detect.roboflow.com/jenwindows-workspace/" + PROJECT_ID + "/1?api_key=" + API_KEY
        
        
        response = requests.post(url, data=img_data)
        
       
        if response.status_code != 200:
            print("Server said: " + response.text)
            return False

        result = response.json()

        
        if "predictions" in result and len(result["predictions"]) > 0:
            print("SUCCESS: AI detected a dog!")
            return True
        
        return False

    except Exception as e:
        print("Python Error: " + str(e))
        return False
