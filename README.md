# AI CTF Challenge: Adversarial Attack on Image Classification

Welcome to the **AI CTF Challenge**! This is a Capture The Flag (CTF) challenge designed to teach participants about **adversarial attacks** on machine learning models, specifically image classifiers. Participants must craft an adversarial image to fool an AI model into misclassifying it.

This challenge is a great example for **classroom training** or **workshops**, as it provides hands-on experience with adversarial machine learning in a controlled environment.

---

## Challenge Overview

### Objective
The goal of this challenge is to craft an adversarial image that causes the AI model to classify it as the "flag" class. Participants will interact with a Flask-based API to submit images and receive predictions.

### Model
The challenge uses a pre-trained **ResNet18** model with three output classes:
- `cat`
- `dog`
- `flag`

Participants must modify an image (e.g., of a cat or dog) so that the model predicts the `flag` class.

---

## Getting Started

### Pull the Docker Image
If you don't want to build the challenge yourself, you can pull the pre-built Docker image from Docker Hub:

```bash
docker pull iven86/ai-ctf-challenge
```

### Run the Docker Container

Once you have the Docker image, run the container:

```bash
docker run -d -p 5000:5000 --network bridge --name ai-ctf-challenge iven86/ai-ctf-challenge
```

## How to Use
### Web Interface

Open your browser and go to http://localhost:5000 to view instructions and example requests.
API Endpoints

- / (GET): Returns an HTML page with instructions and example requests.

- /classify (POST): Accepts an image file and returns the model's prediction or the flag.

- /hint (GET): Provides hints to participants.

Example Requests
Using curl

```bash
curl -X POST -F "image=@path/to/your/image.jpg" http://localhost:5000/classify
```

### Using Python

```python
import requests

url = "http://localhost:5000/classify"
files = {"image": open("path/to/your/image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Using Postman

- Set the request type to POST.

- Set the URL to http://localhost:5000/classify.

- Go to the Body tab, select form-data, and add a key named image with the image file as the value.

### Hints

If you're stuck, you can request hints by sending a GET request to /hint:

```bash
curl http://localhost:5000/hint?attempt=0 # Provide the number of attempts you've made
```

## Why This Challenge?

This CTF challenge is an excellent tool for:

- Teaching adversarial machine learning concepts.

- Hands-on training for students in AI/ML workshops or classes.

- Understanding how image classifiers can be fooled with adversarial examples.

