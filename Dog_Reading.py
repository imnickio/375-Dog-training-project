import base64
import requests
import pygame
import pygame.camera
import time

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
# Using the Public COCO model to avoid workspace permission issues
URL = "https://detect.roboflow.com/coco/3"

def capture_image(filename="scan.jpg"):
    """Captures a frame from the USB camera."""
    try:
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam.start()
        # Give the camera a split second to adjust to light
        time.sleep(0.1)
        img = cam.get_image()
        pygame.image.save(img, filename)
        cam.stop()
        return True
    except Exception as e:
        print(f"Camera Error: {e}")
        return False

def is_dog_present():
    """Returns True if a dog is detected in the kitchen."""
    if not capture_image():
        return False

    # 1. Prepare the image as a Base64 string (Required by Roboflow API)
    with open("scan.jpg", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    # 2. Set up the API call
    params = {"api_key": API_KEY}
    
    try:
        # 3. Send the request
        response = requests.post(URL, params=params, data=img_base64, timeout=10)
        
        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            for p in predictions:
                # Filter for 'dog' and ensure it's at least 40% confident
                if p['class'] == 'dog' and p['confidence'] > 0.4:
                    print(f"Dog detected! Confidence: {p['confidence']:.2f}")
                    return True
            print("No dog in frame.")
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Network Error: {e}")
        
    return False
