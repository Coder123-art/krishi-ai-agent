  ┌────────────────────────────┐
                 │      Farmer Interface      │
                 │        (Streamlit)         │
                 │  - Inputs (NPK, city)     │
                 │  - Image upload           │
                 │  - Voice output (gTTS)    │
                 └────────────┬──────────────┘
                              │ HTTP (REST)
                              ▼
                 ┌────────────────────────────┐
                 │        API Gateway         │
                 │        (FastAPI)           │
                 │  - /soil_analysis          │
                 │  - /weather_real           │
                 │  - /market_price           │
                 │  - /detect_disease         │
                 └────────────┬──────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌──────────────────┐
│  Soil Agent    │  │ Weather Agent  │  │  Market Agent    │
│  (Rule/ML)     │  │ (API Logic)    │  │ (Trend/Logic)    │
│ - NPK analysis │  │ - OpenWeather  │  │ - Price predict  │
│ - Fertilizer   │  │ - Irrigation   │  │ - Demand trend   │
└────────────────┘  └────────────────┘  └──────────────────┘
          │                   │                   │
          └────────────┬──────┴──────────────┬────┘
                       ▼                     ▼
               ┌────────────────┐   ┌────────────────────┐
               │ Disease Agent  │   │  Voice Engine      │
               │ (Image Model)  │   │   (gTTS)           │
               │ - CNN / Mock   │   │ - Hindi/English    │
               │ - Treatment    │   │ - Audio response   │
               └────────────────┘   └────────────────────┘
                              │
                              ▼
                 ┌────────────────────────────┐
                 │     Response Composer      │
                 │  - Merge outputs           │
                 │  - Format JSON             │
                 └────────────┬──────────────┘
                              │
                              ▼
                 ┌────────────────────────────┐
                 │     Final Advisory         │
                 │  - Fertilizer advice       │
                 │  - Irrigation plan         │
                 │  - Market decision         │                                                                                                                              
                 │  - Disease treatment       │
                 └────────────────────────────┘
🔧 Data Flow
User → Streamlit UI → FastAPI → Agents (Soil/Weather/Market/Disease)
→ Response Composer → JSON → Streamlit → Voice Output + Display


🧠 Key Components
Frontend: Streamlit (UI + Voice Playback)
Backend: FastAPI (API Gateway)
Agents:
Soil Intelligence (NPK logic)
Weather Intelligence (API-based)
Market Intelligence (trend logic)
Disease Detection (image model)
Voice Engine: gTTS
External API: OpenWeather


⚙️ Deployment View
[ User Browser ]
        │
        ▼
[ Streamlit App (Port 8501) ]
        │
        ▼
[ FastAPI Server (Port 8000) ]
        │
        ▼
[ AI Agents + External APIs ]
