import base64
import requests
import pygame
import pygame.camera
import time

# --- CONFIGURATION ---
API_KEY = "2DqULRG06WgrWpX6WSwC"
MODEL_ID = "coco/3"
URL = "https://detect.roboflow.com/{}".format(MODEL_ID)

def capture_image(filename="scan.jpg"):
    try:
        pygame.camera.init()
        cam = pygame.camera.Camera("/dev/video0", (640, 480))
        cam.start()
        time.sleep(0.1)
        img = cam.get_image()
        pygame.image.save(img, filename)
        cam.stop()
        return True
    except Exception as e:
        print("Camera Error: {}".format(e))
        return False

def is_dog_present(*args):
    if not capture_image():
        return False

    with open("scan.jpg", "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    params = {"api_key": API_KEY}
    
    try:
        response = requests.post(URL, params=params, data=img_base64, timeout=10)
        
        if response.status_code == 200:
            predictions = response.json().get("predictions", [])
            for p in predictions:
                if p['class'] == 'dog' and p['confidence'] > 0.4:
                    print("Dog detected! Confidence: {}".format(p['confidence']))
                    return True
            print("No dog in frame.")
        else:
            print("API Error: {} - {}".format(response.status_code, response.text))
            
    except Exception as e:
        print("Network Error: {}".format(e))
        
    return False
