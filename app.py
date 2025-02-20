from flask import Flask, request, jsonify, render_template_string
import torch
import torchvision.transforms as transforms
from PIL import Image
import torchvision.models as models
import torch.nn as nn

app = Flask(__name__)

# Define the model architecture
model = models.resnet18(weights=None)  # Don't load pre-trained weights
num_classes = 3  # Same as during training
model.fc = nn.Linear(model.fc.in_features, num_classes)  # Modify the final layer

# Load the state dictionary
model.load_state_dict(torch.load("model.pth"))

# Set the model to evaluation mode
model.eval()

# Preprocess input image
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)

# Hints for participants
hints = [
    "Try modifying the image slightly to fool the model.",
    "Research adversarial attacks on image classifiers.",
    "Use a library like foolbox to generate adversarial examples.",
]

# Class labels (add "flag" as the target class)
class_labels = ["cat", "dog", "flag"]

# Root route: Serve an HTML page with API instructions
@app.route("/", methods=["GET"])
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AI CTF Challenge</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }
                .container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    max-width: 800px;
                    width: 100%;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #555;
                    line-height: 1.6;
                }
                pre {
                    background-color: #f8f9fa;
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                }
                code {
                    color: #d63384;
                }
                a {
                    color: #007bff;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>AI CTF Challenge</h1>
                <p>
                    Welcome to the AI CTF Challenge! Your goal is to fool an AI model into misclassifying an image.
                    Use the API endpoint below to submit images and get predictions.
                </p>
                <p>
                    The model classifies images into three categories: <code>cat</code>, <code>dog</code>, and <code>flag</code>.
                    Your task is to craft an image that the model classifies as <code>flag</code>.
                </p>
                <h2>API Endpoint</h2>
                <p>
                    Send a <strong>POST</strong> request to <code>/classify</code> with an image file to get the model's prediction.
                </p>
                <h3>Example Requests</h3>
                <p>Using <code>curl</code>:</p>
                <pre>
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/classify
                </pre>
                <p>Using Python:</p>
                <pre>
import requests

url = "http://localhost:5000/classify"
files = {"image": open("path/to/your/image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
                </pre>
                <p>Using Postman:</p>
                <ol>
                    <li>Set the request type to <strong>POST</strong>.</li>
                    <li>Set the URL to <code>http://localhost:5000/classify</code>.</li>
                    <li>Go to the <strong>Body</strong> tab, select <strong>form-data</strong>, and add a key named <code>image</code> with the image file as the value.</li>
                </ol>
                <h2>Hints</h2>
                <p>
                    If you're stuck, you can request hints by sending a <strong>GET</strong> request to <code>/hint</code>.
                </p>
                <p>Example:</p>
                <pre>
curl http://localhost:5000/hint?attempt=0
                </pre>
                <p>
                    Replace <code>0</code> with the attempt number to get different hints.
                </p>
                <h2>Good Luck!</h2>
                <p>
                    Use tools like <a href="https://foolbox.readthedocs.io/" target="_blank">Foolbox</a> to generate adversarial examples.
                </p>
            </div>
        </body>
        </html>
    ''')

# Hint endpoint
@app.route("/hint", methods=["GET"])
def hint():
    attempt = request.args.get("attempt", default=0, type=int)
    return jsonify({"hint": hints[min(attempt, len(hints) - 1)]})

# Classify endpoint
@app.route("/classify", methods=["POST"])
def classify():
    # Get image from request
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files["image"]
    try:
        image = Image.open(file.stream).convert("RGB")
        input_tensor = preprocess_image(image)
    except Exception as e:
        return jsonify({"error": f"Invalid image file: {str(e)}"}), 400

    # Perform inference
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
        predicted_class = class_labels[predicted.item()]

    # Check if the prediction is the target class
    if predicted_class == "flag":
        return jsonify({"flag": "CTF{adversarial_attack_successful}"})
    else:
        return jsonify({"prediction": predicted_class})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
