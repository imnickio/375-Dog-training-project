import subprocess
import os
import base64
import requests
import gc


def capture_image(filename="scan.jpg"):

    subprocess.run(["sudo", "fuser", "-k", "/dev/video0"], stderr=subprocess.DEVNULL)
    
    if os.path.exists(filename):
        os.remove(filename)

    try:
        
        subprocess.run([
            "fswebcam", "-r", "640x480", "--no-banner", "-F", "1", "-S", "30", filename
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return os.path.exists(filename)
    except Exception:
        return False


def get_dog_pose():
    if not capture_image(): 
        return "nothing"


    API_KEY = "NPwSzzX6IxxvAsFWXWm1"
    MODEL_ID = "dog-pose-ahfet/1"
    URL = f"https://classify.roboflow.com/{MODEL_ID}?api_key={API_KEY}"

    try:
        with open("scan.jpg", "rb") as f:
            img_data = base64.b64encode(f.read()).decode('utf-8')

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(URL, data=img_data, headers=headers, timeout=10)
        
        img_data = None
        gc.collect() 

        if response.status_code == 200:
            res = response.json()
       
            if isinstance(res, list):
                if len(res) > 0:
                    return res[0].get('class', 'nothing')
                return "nothing"
            return res.get("top", "nothing")
            
        return "nothing"
    except Exception:
        return "nothing"
