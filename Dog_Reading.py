from inference_sdk import InferenceHTTPClient
import os


client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="AU8JxB1DTPRTyxA9qcqL" 
)

def check_for_dog(image_path):

    if not os.path.exists(image_path):
        print("Error: Image file not found for AI analysis.")
        return False

    try:
        
        result = client.run_workflow(
            workspace_name="jenwindows-workspace",
            workflow_id="find-dogs",
            images={"image": image_path},
            use_cache=True
        )

        
        predictions = result[0]["model_predictions"]["predictions"]
        
       
        return len(predictions) > 0

    except Exception as e:
        print(f"AI Error: {e}")
        return False
