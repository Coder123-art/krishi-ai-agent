## 🏗 System Architecture

```mermaid
flowchart TD

A[Farmer (Streamlit UI)]
A -->|Inputs (NPK, city, image)| B[FastAPI Backend]

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
H --> J[Voice Output (gTTS)]
## 🏗 Architectural View

```mermaid
flowchart LR

%% ----------- Presentation Layer -----------
subgraph L1["Presentation Layer"]
UI[Streamlit UI<br/>- Inputs (NPK, City)<br/>- Image Upload<br/>- Voice Output]
end

%% ----------- API Layer -----------
subgraph L2["API Layer"]
API[FastAPI Gateway<br/>REST Endpoints]
end

%% ----------- Intelligence Layer -----------
subgraph L3["AI / Agent Layer"]
S[Soil Agent<br/>NPK Analysis]
W[Weather Agent<br/>OpenWeather API]
M[Market Agent<br/>Price Prediction]
D[Disease Agent<br/>Image Model]
end

%% ----------- Processing Layer -----------
subgraph L4["Processing Layer"]
R[Response Composer<br/>Merge + JSON]
V[Voice Engine (gTTS)]
end

%% ----------- Output Layer -----------
subgraph L5["Output Layer"]
O[Final Advisory<br/>Fertilizer + Irrigation + Market + Treatment]
end

%% ----------- Connections -----------
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