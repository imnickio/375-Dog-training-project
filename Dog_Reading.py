import os
import json

# Use the PRIVATE Key here
API_KEY = "2DqULRG06WgrWpX6WSwC" 
PROJECT_ID = "find-dogs-tuzes-instant/1"

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False

    # The -k tells curl to IGNORE old security certificates (Fixes 403/SSL errors)
    # The -s makes it quiet
    # The -d @path sends the image data directly
    url = "https://detect.roboflow.com/" + PROJECT_ID + "?api_key=" + API_KEY
    command = "curl -k -s -X POST '" + url + "' --data-binary @" + image_path
    
    try:
        # Run the command and capture the text it spits out
        response_text = os.popen(command).read()
        
        # If the server is still mad, it will print the error here
        if "Forbidden" in response_text or "Unauthorized" in response_text:
            print("AI Access Denied: Check if the API Key is copied correctly!")
            return False

        # Turn the text into a Python list
        result = json.loads(response_text)

        if "predictions" in result and len(result["predictions"]) > 0:
            print("AI SUCCESS: Spotted a " + str(result["predictions"][0]["class"]))
            return True
            
        return False

    except Exception as e:
        print("System Error: " + str(e))
        return False
