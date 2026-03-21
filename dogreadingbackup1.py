# Run this first command in powershell, will make python use 3.11 to install
# py -3.11 -m pip install inference-sdk
# Run this command in terminal in, change the image to whatever file path/website you want, use "/" instead of "\" or youll get issues
# py -3.11 Dog_Reading.py

# 1. Import the library
from inference_sdk import InferenceHTTPClient

# 2. Connect to your workflow
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="AU8JxB1DTPRTyxA9qcqL"
)

# 3. Run your workflow on an image
result = client.run_workflow(
    workspace_name="jenwindows-workspace",
    workflow_id="find-dogs",
    images={
        "image": "C:/Users/jenwi/Downloads/images.jpg" # Path to your image file
    },
    use_cache=True # Speeds up repeated requests
)

# 4. Get your results
print(result[0]["model_predictions"]["predictions"])
