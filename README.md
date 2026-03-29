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

## 🏗 System Architecture

```mermaid
flowchart TD

A[Farmer (Streamlit UI)]
A --> B[FastAPI Backend]

B --> C[Soil Agent]
B --> D[Weather Agent]
B --> E[Market Agent]
B --> F[Disease Agent]

C --> G[Response Composer]
D --> G
E --> G
F --> G

G --> H[Final Advisory Output]

H --> I[UI Display]
H --> J[Voice Output (gTTS)
```

---

## 🏗 Architectural View

```mermaid
flowchart LR

subgraph Presentation
UI[Streamlit UI]
end

subgraph API
API[FastAPI Gateway]
end

subgraph Agents
S[Soil Agent]
W[Weather Agent]
M[Market Agent]
D[Disease Agent]
end

subgraph Processing
R[Response Composer]
V[Voice Engine]
end

subgraph Output
O[Final Advisory]
end

UI --> API
API --> S
API --> W
API --> M
API --> D

S --> R
W --> R
M --> R
D --> R

R --> O
O --> V
O --> UI
```

---

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
