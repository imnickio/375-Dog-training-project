import requests
import base64
import os

# Your friend's API details
API_KEY = "AU8JxB1DTPRTyxA9qcqL"
WORKFLOW_ID = "find-dogs"
WORKSPACE = "jenwindows-workspace"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        # 1. Read the image and encode it for the internet
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

        # 2. Build the request URL for Roboflow's API
        url = "https://detect.roboflow.com/dog-detection/1" # Generic dog model URL
        params = {
            "api_key": API_KEY
        }

        # 3. Send the image to the cloud
        response = requests.post(url, params=params, data=img_data)
        result = response.json()

        # 4. Check if a dog was found
        # Roboflow returns a list of 'predictions'
        if "predictions" in result and len(result["predictions"]) > 0:
            # You can even check confidence here (e.g., > 0.5)
            print("AI found a dog with " + str(result['predictions'][0]['confidence']) + " confidence")
            return True
        
        return False

    except Exception as e:
        print("Network/AI Error: " + str(e))
        return False
