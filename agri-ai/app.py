import streamlit as st
import requests
from gtts import gTTS
import os

# ---------------- VOICE FUNCTION (NO ERROR VERSION) ----------------
def speak(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")

    audio_file = open("voice.mp3", "rb")
    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3")

# ---------------- UI ----------------
st.title("🌾 KrishiSahayak AI Agent")
st.markdown("AI-powered smart farming system 🚀")

# 🌐 Language Selector
language = st.selectbox("🌐 Select Language", ["English", "Hindi"])
lang_code = "hi" if language == "Hindi" else "en"

voice_on = st.checkbox("🔊 Enable Voice")
# =====================================================
st.header("🌱Soil Analysis")
# =====================================================

n = st.slider("Nitrogen",0,100)
p = st.slider("Phosphorus",0,100)
k = st.slider("Potassium",0,100)

if st.button("Analyze Soil"):
    try:
        res = requests.post(
            "http://127.0.0.1:8000/soil_analysis",
            params={"nitrogen": n, "phosphorus": p, "potassium": k}
        )

        data = res.json()

        st.subheader(data["soil_health"])

        for item in data["details"]:
            st.write(item)
         # 🔊 Voice
        if voice_on:
            if language == "Hindi":
                speak("मिट्टी की जांच पूरी हो गई है", lang_code)
            else:
                speak("Soil analysis completed", lang_code)

    except Exception as e:
        st.error(f"Error: {e}")
    


# =====================================================
st.header("🌥️ Weather Advice")
# =====================================================

city = st.text_input("Enter City", "Delhi")

if st.button("Get Weather"):

    try:
        res = requests.get(
            "http://127.0.0.1:8000/weather_real",
            params={"city": city}
        )

        data = res.json()

        # ❌ handle error
        if "error" in data:
            st.error(data["error"])

        else:
            st.subheader(f"🌍 City: {data['city']}")
            st.write(f"🌡 Temperature: {data['temperature']} °C")
            st.write(f"💧 Humidity: {data['humidity']} %")
            st.write(f"🌧 Rainfall: {data['rainfall']} mm")

            st.success(data["advice"])
        # 🔊 Voice
            if voice_on:
                if language == "Hindi":
                    speak(f"{city} का तापमान {data['temperature']} डिग्री है", lang_code)
                else:
                    speak(f"The temperature in {city} is {data['temperature']} degrees", lang_code)


    except:
        st.error("❌ Backend not running or connection failed")

# =====================================================       
st.header("📊 Market Price")
# =====================================================
crop = st.selectbox(
    "Select Crop",
    [
        "Wheat","Rice","Maize","Sweetcorn","Sweetpotato",
        "Sugarcane","Cotton","Soybean","Groundnut","Sunflower",
        "Jujube","Guava","Mango","Banana","Orange","Grapes"
    ]
)

if st.button("Predict Price"):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/market_price",
            params={"crop": crop}
        )

        data = res.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.subheader(f"🌾 {data['crop']}")

            st.write(f"💵 Base Price: ₹{data['base_price']}")
            st.write(f"💰 Predicted Price: ₹{data['predicted_price']}")
            st.write(f"📊 Trend: {data['market_trend']}")

            # smart suggestion
            if "High Demand" in data["market_trend"]:
                st.success("🚀 Best time to sell!")
            elif "Increasing" in data["market_trend"]:
                st.info("👍 Prices improving, consider selling soon")
            else:
                st.warning("⚠️ Prices dropping, wait before selling")
             # 🔊 Voice
            if voice_on:
                if language == "Hindi":
                    speak(f"{crop} का भाव {data['predicted_price']} रुपये है", lang_code)
                else:
                    speak(f"The price of {crop} is {data['predicted_price']} rupees", lang_code)

    except Exception as e:
        st.error(f"Error: {e}")
# =====================================================
st.header("🌿 Crop Disease Detection")
# =====================================================
# 📸 Upload image
image = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"])

if st.button("Detect Disease"):

    if image is None:
        st.error("❌ Please upload an image first")

    else:
        try:
            # send image to backend
            files = {"file": image.getvalue()}

            res = requests.post(
                "http://127.0.0.1:8000/detect_disease",
                files=files
            )

            data = res.json()

            # ❌ error handling
            if "error" in data:
                st.error(data["error"])

            else:
                # show image
                st.image(image, caption="Uploaded Leaf", use_column_width=True)

                # show result
                st.success(f"🌿 Disease: {data['disease']}")
                st.info(f"💊 Treatment: {data['treatment']}")

                # 🔊 AUDIO FIX (important)
                try:
                    with open(data["audio"], "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")
                except:
                    st.warning("🔊 Audio playback not available")

        except:
            st.error("❌ Backend not running or connection failed")