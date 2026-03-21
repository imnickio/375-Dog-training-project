import requests
import base64
import os

API_KEY = "AU8JxB1DTPRTyxA9qcqL"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

       
        url = "https://detect.roboflow.com/dog-detection/1"
        
        params = {
            "api_key": API_KEY,
            "confidence": 40  # 40% confidence threshold
        }

      
        response = requests.post(url, params=params, data=img_data)
        
      
        if response.status_code != 200:
            print("Server Busy (Error " + str(response.status_code) + ")")
            return False

        result = response.json()

        if "predictions" in result and len(result["predictions"]) > 0:
            print("Dog Found! Confidence: " + str(result['predictions'][0]['confidence']))
            return True
        
        return False

    except Exception as e:
        print("Network hiccup: " + str(e))
        return False
