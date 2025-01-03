from google.cloud import aiplatform
import os

# Set up Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Initialize the AI Platform Prediction Service Client
client = aiplatform.gapic.PredictionServiceClient()

# Define the endpoint
endpoint_name = "projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/endpoints/YOUR_ENDPOINT_ID"

def get_image_description(image_path):
    """
    Sends an image to the AI platform for description generation.
    """
    # Ensure the image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    # Read the image as binary data
    with open(image_path, "rb") as image_file:
        image_content = image_file.read()

    # Prepare the instance for prediction
    instance = {"image": {"bytes": image_content}}
    instances = [instance]

    # Make the prediction using the endpoint name
    response = client.predict(endpoint=endpoint_name, instances=instances)

    # Parse and return the first prediction result
    predictions = response.predictions
    return predictions[0].get("description", "No description found")

def extract_keywords(description):
    """
    Extracts keywords from the image description.
    """
    return [word.strip() for word in description.split() if len(word) > 3]

# Example usage
if __name__ == "__main__":
    try:
        # Path to the input image
        image_path = "example.jpg"

        # Generate the image description
        description = get_image_description(image_path)
        print("Image Description:", description)

        # Extract keywords
        keywords = extract_keywords(description)
        print("Keywords:", keywords)

    except Exception as e:
        print("Error:", e)
