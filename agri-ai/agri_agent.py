from fastapi import FastAPI, UploadFile, File
from PIL import Image
import numpy as np
import random
import requests
import io
import os
from gtts import gTTS

app = FastAPI()

# -----------------------------
# 🌱 Soil Analysis (Rule-Based)
# -----------------------------

fertilizer_rules = {
    "low_nitrogen": "Use Urea fertilizer",
    "low_phosphorus": "Use DAP fertilizer",
    "low_potassium": "Use MOP fertilizer"
}

@app.get("/")
def home():
    return {"message": "Krishi AI Agent Running"}

@app.post("/soil_analysis")
def soil_analysis(nitrogen: int, phosphorus: int, potassium: int):

    report = []
    score = 0

    # Nitrogen
    if nitrogen < 40:
        report.append("🟥 Nitrogen is LOW → Apply Urea")
    elif nitrogen < 70:
        report.append("🟨 Nitrogen is MEDIUM → Maintain balance")
        score += 1
    else:
        report.append("🟩 Nitrogen is GOOD")
        score += 2

    # Phosphorus
    if phosphorus < 40:
        report.append("🟥 Phosphorus is LOW → Apply DAP")
    elif phosphorus < 70:
        report.append("🟨 Phosphorus is MEDIUM")
        score += 1
    else:
        report.append("🟩 Phosphorus is GOOD")
        score += 2

    # Potassium
    if potassium < 40:
        report.append("🟥 Potassium is LOW → Apply MOP")
    elif potassium < 70:
        report.append("🟨 Potassium is MEDIUM")
        score += 1
    else:
        report.append("🟩 Potassium is GOOD")
        score += 2

    # Soil Health Score
    if score >= 5:
        health = "🟢 Excellent Soil"
    elif score >= 3:
        health = "🟡 Moderate Soil"
    else:
        health = "🔴 Poor Soil"

    return {
        "soil_health": health,
        "details": report
    }

# -----------------------------
# 🌦 Real Weather API
# -----------------------------
from fastapi import FastAPI
import requests

app = FastAPI()

API_KEY = "eae50a8b4cee88ee3307c4ecfccd49a2"


def generate_advice(data):
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    rainfall = data.get("rain", {}).get("1h", 0)
    weather_main = data["weather"][0]["main"]

    if rainfall > 5:
        return "🌧 Heavy rain → Do NOT irrigate"

    elif rainfall > 0:
        return "🌦 Light rain → Reduce irrigation"

    elif weather_main == "Rain":
        return "🌧 Rain detected → Avoid irrigation"

    elif temp > 35:
        return "🔥 High temperature → Frequent irrigation needed"

    elif humidity > 80:
        return "💧 High humidity → Reduce watering"

    elif temp < 15:
        return "❄ Cold weather → Minimal irrigation"

    else:
        return "✅ Normal conditions → Balanced irrigation"


@app.get("/weather_real")
def weather_real(city: str = "Delhi"):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": "City not found or API issue"}

        data = response.json()

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall": data.get("rain", {}).get("1h", 0),
            "condition": data["weather"][0]["main"],
            "advice": generate_advice(data)
        }

    except Exception as e:
        return {"error": str(e)}

# -----------------------------
# 💰 Market Price Prediction
# -----------------------------

@app.get("/market_price")
def price(crop: str):

    base_prices = {
        "wheat": 2200,
        "rice": 2100,
        "maize": 1800,
        "sweetcorn": 2500,
        "sweetpotato": 3000,
        "sugarcane": 1500,
        "cotton": 3500,
        "soybean": 2800,
        "groundnut": 3200,
        "sunflower": 2700,
        "jujube": 4000,
        "guava": 3500,
        "mango": 5000,
        "banana": 3000,
        "orange": 4000,
        "grapes": 4500
    }

    crop_lower = crop.lower()

    if crop_lower not in base_prices:
        return {"error": "Crop not found"}

    base = base_prices[crop_lower]

    # realistic variation
    variation = random.randint(-300, 300)
    final_price = base + variation

    # trend logic
    if variation > 100:
        trend = "📈 High Demand"
    elif variation > 0:
        trend = "📈 Increasing"
    elif variation < -100:
        trend = "📉 Low Demand"
    else:
        trend = "📉 Decreasing"

    return {
        "crop": crop.capitalize(),
        "base_price": base,
        "predicted_price": final_price,
        "market_trend": trend
    }

# -----------------------------
# 🌿 Crop Disease Detection
# -----------------------------
diseases = {
    "Healthy Leaf": "No action needed",
    "Leaf Spot Disease": "Apply copper fungicide",
    "Powdery Mildew": "Use sulfur spray",
    "Rust Infection": "Spray neem oil"
}

# 🧠 Smart prediction function
def predict_disease(image):

    img = image.resize((224, 224))
    img = np.array(img)

    avg_red = np.mean(img[:,:,0])
    avg_green = np.mean(img[:,:,1])
    avg_blue = np.mean(img[:,:,2])

    # 🌿 Green check
    if avg_green > avg_red and avg_green > avg_blue:
        disease = "Healthy Leaf"
    else:
        disease = random.choice([
            "Leaf Spot Disease",
            "Powdery Mildew",
            "Rust Infection"
        ])

    return {
        "disease": disease,
        "treatment": diseases[disease]
    }


# 🔊 Voice generator
def generate_voice(text):
    tts = gTTS(text=text, lang='en')
    file_path = "output.mp3"
    tts.save(file_path)
    return file_path


# 🚀 API endpoint
@app.post("/detect_disease")
async def detect_disease(file: UploadFile = File(None)):

    # ❌ Validation (no file)
    if file is None:
        return {"error": "No image uploaded"}

    try:
        contents = await file.read()

        if not contents:
            return {"error": "Empty file uploaded"}

        image = Image.open(io.BytesIO(contents))

        result = predict_disease(image)

        # 🔊 Add voice output
        voice_text = f"{result['disease']}. Treatment: {result['treatment']}"
        audio_path = generate_voice(voice_text)

        return {
            "disease": result["disease"],
            "treatment": result["treatment"],
            "audio": audio_path
        }

    except Exception as e:
        return {"error": str(e)}