from google.cloud import vision
import os

# Set up Google Cloud authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# Initialize Vision API client
client = vision.ImageAnnotatorClient()

def get_image_description(image_path):
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    # Generate a brief description using the top labels
    labels = [label.description for label in response.label_annotations[:5]]
    return "This image contains: " + ", ".join(labels)

if __name__ == "__main__":
    image_path = "example.jpg"
    try:
        description = get_image_description(image_path)
        print("Image Description:", description)
    except Exception as e:
        print("Error:", e)
