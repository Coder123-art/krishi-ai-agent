import numpy as np
from PIL import Image

def predict_disease(image_file):

    img = Image.open(image_file).resize((224, 224))
    img = np.array(img)

    # average color channels
    avg_red = np.mean(img[:,:,0])
    avg_green = np.mean(img[:,:,1])
    avg_blue = np.mean(img[:,:,2])

    # 🌿 Smart logic
    if avg_green > avg_red and avg_green > avg_blue:
        # Mostly green → healthy
        return "🌿 Healthy Leaf (No disease detected)"

    else:
        diseases = [
            "🟤 Leaf Spot Disease",
            "⚪ Powdery Mildew",
            "🟠 Rust Infection"
        ]

        # pick disease only if unhealthy
        return np.random.choice(diseases)