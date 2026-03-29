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
H --> J[Voice Output (gTTS)]

---

```markdown
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