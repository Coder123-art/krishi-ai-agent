                ┌──────────────────────┐
                │      USER (Farmer)   │
                │  Web / Mobile UI     │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │  Streamlit Frontend  │
                │  (app.py)            │
                │ - UI Inputs          │
                │ - Voice Output       │
                └─────────┬────────────┘
                          │ API Calls
                          ▼
                ┌──────────────────────┐
                │   FastAPI Backend    │
                │   (agri_agent.py)    │
                └─────────┬────────────┘
                          │
      ┌───────────────┬───────────────┬───────────────┬
      ▼               ▼               ▼               ▼
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ Soil       │ │ Weather    │ │ Market     │ │ Disease    │
│ Analysis   │ │ API        │ │ Prediction │ │ Detection  │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
      │               │               │               │
      ▼               ▼               ▼               ▼
 Simple Logic   OpenWeather API   Price Logic   Image Processing
 (NPK based)                      (Random/Trend) (NumPy + PIL)
                                                   │
                                                   ▼
                                          disease_model.py

                          ▼
                ┌──────────────────────┐
                │  Response Generator  │
                │ JSON + Voice (gTTS)  │
                └─────────┬────────────┘
                          ▼
                ┌──────────────────────┐
                │  Streamlit Display   │
                │  Text + Audio Output │
                └──────────────────────┘
🏗️ System Architecture – KrishiSahayak AI Agent

KrishiSahayak follows a modular client-server architecture designed for scalability and simplicity.

1. Frontend Layer

The frontend is built using Streamlit, which provides an interactive interface for farmers.
Users can input soil data, upload crop images, check weather, and view market prices.
It also supports voice output using text-to-speech for better accessibility.

2. Backend Layer

The backend is implemented using FastAPI, which handles all business logic and API routing.
The frontend communicates with the backend through HTTP requests.

3. Core Modules
Soil Analysis Module
Uses NPK values to determine soil health and provides fertilizer recommendations.
Weather Module
Fetches real-time weather data from an external API and generates farming advice.
Market Price Module
Simulates crop price trends and helps farmers decide the best time to sell.
Disease Detection Module
Processes uploaded leaf images using NumPy and PIL to detect possible diseases.
4. AI / Processing Layer

The disease detection logic is implemented in a separate file (disease_model.py), ensuring modularity and easy future upgrades to ML models.

5. Response Layer

The backend returns structured JSON responses, which are displayed on the frontend.
Additionally, gTTS (Google Text-to-Speech) is used to convert results into audio.

6. Error Handling
API failures handled with try-except blocks
User-friendly error messages displayed in UI
Backend validation ensures correct inputs
