# 🌾 KrishiSahayak AI Agent

AI-powered smart farming assistant for Indian farmers.

---

## 🚀 Features

* 🌱 Soil Analysis (NPK-based)
* 🌦 Weather Advisory
* 💰 Market Price Prediction
* 🌿 Crop Disease Detection
* 🔊 Voice Output (Hindi + English)

---
## 🏗 System Architecture (Agent-Oriented)
## 🏗 System Architecture (Agent-Oriented)

```mermaid
flowchart LR

%% -------- Layers --------
subgraph Presentation
UI[Streamlit UI<br/>Inputs: NPK, City, Image<br/>Outputs: Text + Voice]
end

subgraph API
API[FastAPI Gateway<br/>soil_analysis<br/>weather_real<br/>market_price<br/>detect_disease]
end

subgraph Agents
S[Soil Agent]
W[Weather Agent]
M[Market Agent]
D[Disease Agent]
end

subgraph Integrations
OW[OpenWeather API]
ML[Image Model or Rules]
DB[(Cache or Config)]
end

subgraph Processing
R[Response Composer<br/>Merge and Validate]
V[Voice Engine gTTS]
end

subgraph Output
O[Final Advisory<br/>Fertilizer, Irrigation, Price, Treatment]
end

%% -------- Flow --------
UI --> API

API --> S
API --> W
API --> M
API --> D

W --> OW
D --> ML
S --> DB
M --> DB

S --> R
W --> R
M --> R
D --> R

R --> O
O --> V
O --> UI
```


## 🔄 Data Flow

User → Streamlit UI → FastAPI → Agents → Response Composer → UI + Voice Output

---

## ⚙️ Tech Stack

* Frontend: Streamlit
* Backend: FastAPI
* Voice: gTTS
* APIs: OpenWeather

---

## ▶️ Run Locally

### Install dependencies

pip install -r requirements.txt

### Run backend

uvicorn agri_agent:app --reload

### Run frontend

streamlit run app.py
