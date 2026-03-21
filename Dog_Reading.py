import requests
import base64
import os
import json


API_KEY = "AU8JxB1DTPRTyxA9qcqL"
WORKSPACE = "jenwindows-workspace"
WORKFLOW_ID = "find-dogs"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
       
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

        
        url = "https://detect.roboflow.com/infer/workflows/" + WORKSPACE + "/" + WORKFLOW_ID
        
        
        payload = {
            "api_key": API_KEY,
            "inputs": {
                "image": img_data
            }
        }

        
        response = requests.post(url, json=payload)
        result = response.json()

        
        print("AI Response: " + str(result))

       
        if "outputs" in result:
            predictions = result["outputs"][0]["model_predictions"]["predictions"]
            if len(predictions) > 0:
                print("Friend's AI detected a dog!")
                return True
        
        return False

    except Exception as e:
        print("Network/AI Error: " + str(e))
        return False
