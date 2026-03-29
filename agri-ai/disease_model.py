import numpy as np
from PIL import Image

# Treatment mapping
treatments = {
    "Healthy Leaf": "No action needed",
    "Leaf Spot Disease": "Apply copper fungicide",
    "Powdery Mildew": "Use sulfur spray",
    "Rust Infection": "Spray neem oil"
}

def predict_disease(image_file):

    img = Image.open(image_file).resize((224, 224))
    img = np.array(img)

    avg_red = np.mean(img[:,:,0])
    avg_green = np.mean(img[:,:,1])
    avg_blue = np.mean(img[:,:,2])

    # 🌿 Smart logic
    if avg_green > avg_red and avg_green > avg_blue:
        disease = "Healthy Leaf"
    else:
        disease = np.random.choice([
            "Leaf Spot Disease",
            "Powdery Mildew",
            "Rust Infection"
        ])

    return {
        "disease": disease,
        "treatment": treatments[disease]
    }