import requests
import base64
import os

API_KEY = "AU8JxB1DTPRTyxA9qcqL"
WORKFLOW_ID = "find-dogs"
WORKSPACE = "jenwindows-workspace"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

       
        url = "https://detect.roboflow.com/dog-detection/1" 
        params = {
            "api_key": API_KEY
        }

        
        response = requests.post(url, params=params, data=img_data)
        result = response.json()
        
        print("AI Response: " + str(result))

        if "predictions" in result:
            for pred in result["predictions"]:
                if pred['class'] == 'dog' and pred['confidence'] > 0.4:
                    print("Found dog! Confidence: " + str(pred['confidence']))
                    return True

        
        return False

    except Exception as e:
        print("Network/AI Error: " + str(e))
        return False
