import os
import requests
import base64

# CONFIG
API_KEY = "NPwSzzX6IxxvAsFWXWm1"
MODEL_ID = "dog-pose-ahfet/1"
URL = f"https://classify.roboflow.com/{MODEL_ID}?api_key=NPwSzzX6IxxvAsFWXWm1"

def test_full_system():
    print("1. Capturing photo...")
    os.system("raspistill -o test.jpg -n -t 500 -w 640 -h 480")
    
    print("2. Sending to AI...")
    with open("test.jpg", "rb") as f:
        img_str = base64.b64encode(f.read()).decode("utf-8")
    
    response = requests.post(URL, data=img_str, 
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    if response.status_code == 200:
        result = response.json().get("top")
        print(f"3. SUCCESS! AI sees: {result}")
    else:
        print(f"3. FAILED. Error: {response.text}")

if __name__ == "__main__":
    test_full_system()
