from inference_sdk import InferenceHTTPClient
import os

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="AU8JxB1DTPRTyxA9qcqL"
)

def is_dog_present(image_path):
    if not os.path.exists(image_path):
        return False
    try:
        result = client.run_workflow(
            workspace_name="jenwindows-workspace",
            workflow_id="find-dogs",
            images={"image": image_path}
        )
        predictions = result[0]["model_predictions"]["predictions"]
        return len(predictions) > 0
    except Exception as e:
        print("AI Error: " + str(e)) # Legacy string style
        return False
