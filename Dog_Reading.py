# Dog_Reading.py (The streamlined version)
def get_dog_pose():
    if not capture_image(): # Your USB camera function
        return "nothing"

    # ... (Your API request code here) ...

    if response.status_code == 200:
        res = response.json()
        # Ensure this returns the string "sit", "lay", or "indoor"
        return res.get("top") 
    return "nothing"
