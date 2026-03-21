import requests
import base64
import os

# Use your API Key (either one should work now)
API_KEY = "2DqULRG06WgrWpX6WSwC" 
# For Public projects, we use the simple ID
PROJECT_ID = "find-dogs-tuzes-instant/1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    try:
        with open(image_path, "rb") as image_file:
            img_data = base64.b64encode(image_file.read()).decode("utf-8")

        # PUBLIC ENDPOINT: Notice we use 'infer.roboflow.com' 
        # instead of 'detect.roboflow.com'
        url = "https://infer.roboflow.com/" + PROJECT_ID
        
        params = {
            "api_key": API_KEY,
            "confidence": "40"
        }

        # Send as a plain string (data=) rather than a JSON object
        response = requests.post(url, params=params, data=img_data)
        
        print("AI Response Code: " + str(response.status_code))
        
        if response.status_code == 200:
            result = response.json()
            if "predictions" in result and len(result["predictions"]) > 0:
                print("SUCCESS: Dog detected in Public Project!")
                return True
        else:
            print("Response text: " + response.text)
            
        return False

    except Exception as e:
        print("Network Error: " + str(e))
        return False

#curl -X POST "https://infer.roboflow.com/find-dogs-tuzes-instant/1?api_key=YOUR_API_KEY" --data-binary @scan.jpg
