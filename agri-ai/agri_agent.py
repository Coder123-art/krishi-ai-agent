from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import random
import requests
from gtts import gTTS

from disease_model import predict_disease

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

# =========================
# 🌱 Soil Analysis API
# =========================
@app.post("/soil_analysis")
def soil_analysis(
    nitrogen: int = Form(...),
    phosphorus: int = Form(...),
    potassium: int = Form(...)
):
    # ✅ calculate score
    score = (nitrogen + phosphorus + potassium) / 3

    details = []
    suggestions = []

    # 🔍 Individual nutrient checks
    if nitrogen < 40:
        details.append("Low Nitrogen detected")
        suggestions.append("Apply Urea fertilizer")

    if phosphorus < 40:
        details.append("Low Phosphorus detected")
        suggestions.append("Use DAP fertilizer")

    if potassium < 40:
        details.append("Low Potassium detected")
        suggestions.append("Use MOP fertilizer")

    # 🌱 Overall soil health
    if score > 70 and not details:
        health = "🟢 Healthy Soil"
        details = [
            "All nutrients are in optimal range",
            "Suitable for most crops",
            "Maintain current practices"
        ]

    elif score > 50:
        health = "🟡 Moderate Soil"
        details.append("Some nutrients need improvement")
        suggestions.append("Use balanced NPK fertilizer")

    else:
        health = "🔴 Poor Soil"
        details.append("Multiple nutrient deficiencies")
        suggestions.append("Add compost and organic matter")

    # 🧠 Combine everything
    final_details = details + suggestions

    return {
        "soil_health": health,
        "details": final_details
    }
# =========================
# 🌥️ Weather API (REAL)
# =========================
API_KEY = "eae50a8b4cee88ee3307c4ecfccd49a2"   # ⚠️ Put your OpenWeatherMap API key here

@app.get("/weather_real")
def weather_real(city: str = "Delhi"):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)

        if response.status_code != 200:
            return {"error": "City not found or API issue"}

        data = response.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        # Simple rainfall logic
        rainfall = data.get("rain", {}).get("1h", 0)

        # Smart advice
        if temp > 35:
            advice = "🌞 High temperature, irrigate crops frequently"
        elif rainfall > 5:
            advice = "🌧 Heavy rain expected, ensure drainage"
        else:
            advice = "🌤 Weather is stable, normal farming conditions"

        return {
            "city": city,
            "temperature": temp,
            "humidity": humidity,
            "rainfall": rainfall,
            "advice": advice
        }

    except:
        return {"error": "Weather service failed"}


# =========================
# 📊 Market Price API
# =========================
@app.get("/market_price")
def market_price(crop: str):

    base_price = random.randint(1000, 5000)
    change = random.randint(-500, 700)

    predicted_price = base_price + change

    if change > 400:
        trend = "📈 High Demand"
    elif change > 0:
        trend = "⬆️ Increasing"
    else:
        trend = "⬇️ Decreasing"

    return {
        "crop": crop,
        "base_price": base_price,
        "predicted_price": predicted_price,
        "market_trend": trend
    }


# =========================
# 🌿 Disease Detection API
# =========================
@app.post("/detect_disease")
async def detect_disease(file: UploadFile = File(...)):
    try:
        # ✅ Call ML model
        result = predict_disease(file.file)

        disease = result["disease"]
        treatment = result["treatment"]

        # 🔊 Generate voice output
        text = f"{disease} detected. Treatment is {treatment}"
        tts = gTTS(text=text, lang="en")
        audio_path = "output.mp3"
        tts.save(audio_path)

        return JSONResponse({
    "disease": disease,
    "treatment": treatment,
    "audio": "voice.mp3"
})

    except Exception as e:
        return {"error": str(e)}