import streamlit as st
import requests
from gtts import gTTS

# ---------------- VOICE FUNCTION ----------------
def speak(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    tts.save("voice.mp3")

    with open("voice.mp3", "rb") as audio_file:
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
st.header("🌱 Soil Analysis")
# =====================================================

n = st.slider("Nitrogen", 0, 100)
p = st.slider("Phosphorus", 0, 100)
k = st.slider("Potassium", 0, 100)

if st.button("Analyze Soil", key="soil"):
    try:
        res = requests.post(
    "http://127.0.0.1:8000/soil_analysis",
    data={"nitrogen": n, "phosphorus": p, "potassium": k},
    timeout=5
)

        data = res.json()

        st.subheader(data["soil_health"])

        for item in data["details"]:
            st.write(item)

        if voice_on:
            speak(
                "मिट्टी की जांच पूरी हो गई है" if language == "Hindi"
                else "Soil analysis completed",
                lang_code
            )

    except Exception as e:
        st.error(f"❌ {e}")


# =====================================================
st.header("🌥️ Weather Advice")
# =====================================================

city = st.text_input("Enter City", "Delhi")

if st.button("Get Weather", key="weather"):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/weather_real",
            params={"city": city},
            timeout=5
        )

        data = res.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.subheader(f"🌍 City: {data['city']}")
            st.write(f"🌡 Temperature: {data['temperature']} °C")
            st.write(f"💧 Humidity: {data['humidity']} %")
            st.write(f"🌧 Rainfall: {data['rainfall']} mm")

            st.success(data["advice"])

            if voice_on:
                speak(
                    f"{city} का तापमान {data['temperature']} डिग्री है" if language == "Hindi"
                    else f"The temperature in {city} is {data['temperature']} degrees",
                    lang_code
                )

    except Exception as e:
        st.error(f"❌ {e}")


# =====================================================
st.header("📊 Market Price")
# =====================================================

crop = st.selectbox(
    "Select Crop",
    [
        "Wheat", "Rice", "Maize", "Sweetcorn", "Sweetpotato",
        "Sugarcane", "Cotton", "Soybean", "Groundnut", "Sunflower",
        "Jujube", "Guava", "Mango", "Banana", "Orange", "Grapes"
    ]
)

if st.button("Predict Price", key="price"):
    try:
        res = requests.get(
            "http://127.0.0.1:8000/market_price",
            params={"crop": crop},
            timeout=5
        )

        data = res.json()

        if "error" in data:
            st.error(data["error"])
        else:
            st.subheader(f"🌾 {data['crop']}")
            st.write(f"💵 Base Price: ₹{data['base_price']}")
            st.write(f"💰 Predicted Price: ₹{data['predicted_price']}")
            st.write(f"📊 Trend: {data['market_trend']}")

            if "High Demand" in data["market_trend"]:
                st.success("🚀 Best time to sell!")
            elif "Increasing" in data["market_trend"]:
                st.info("👍 Prices improving, consider selling soon")
            else:
                st.warning("⚠️ Prices dropping, wait before selling")

            if voice_on:
                speak(
                    f"{crop} का भाव {data['predicted_price']} रुपये है" if language == "Hindi"
                    else f"The price of {crop} is {data['predicted_price']} rupees",
                    lang_code
                )

    except Exception as e:
        st.error(f"❌ {e}")


# =====================================================
st.header("🌿 Crop Disease Detection")
# =====================================================

image = st.file_uploader("Upload leaf image", type=["jpg", "png", "jpeg"])

if st.button("Detect Disease", key="disease"):

    if image is None:
        st.error("❌ Please upload an image first")

    else:
        try:
            files = {"file": ("leaf.jpg", image.getvalue(), "image/jpeg")}

            res = requests.post(
                "http://127.0.0.1:8000/detect_disease",
                files=files,
                timeout=10
            )

            data = res.json()

            if "error" in data:
                st.error(data["error"])
            else:
                st.image(image, caption="Uploaded Leaf", width=500)

                st.success(f"🌿 Disease: {data['disease']}")
                st.info(f"💊 Treatment: {data['treatment']}")

                # 🔊 Voice (NEW — based on disease)
                if voice_on:
                    speak(
                        f"{data['disease']} detected. Treatment is {data['treatment']}"
                        if language == "English"
                        else f"{data['disease']} पाया गया है। उपचार है {data['treatment']}",
                        lang_code
                    )

        except Exception as e:
            st.error(f"❌ {e}")