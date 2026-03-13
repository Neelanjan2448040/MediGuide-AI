# MediGuide AI – Intelligent Health Assistant

MediGuide AI is a premium, full-stack AI health dashboard built for professional medical assistance. It features a robust multi-modal architecture with real-time emergency detection, persistent memory, and advanced analytics.

## 🚀 Key Features
- **Intelligent RAG Assistant**: Securely analyzes medical PDFs and provides grounded clinical guidance using Groq (LLAMA 3.3).
- **Emergency Guard**: Real-time detection of critical symptoms (English/Hinglish) with high-visibility red alerts.
- **Multilingual Support**: Seamlessly transitions between English and Hinglish to suit user preference.
- **Response Modes**: Toggle between **Concise**, **Detailed** (Dietary plans), and **Explain Like I'm 10** for varied scenarios.
- **Consultation Registry**: Integrated SQLite booking system to track and manage clinical appointments.
- **Intelligence Dashboard**: Advanced Plotly visualizations for population health trends and system coverage.
- **Secure Persistence**: User conversations and medical schedules are persisted across sessions.

## 📂 Project Structure
Matching the recommended modular architecture:
```
project/
├── config/
│   └── config.py        # API Keys & System Settings
├── models/
│   ├── llm.py           # LLM core (Groq/LangChain)
│   └── embeddings.py    # RAG Vector definitions
├── utils/
│   ├── rag_manager.py   # Document processing & Retrieval
│   └── search_manager.py# Web fallback logic
├── database/
│   └── db_manager.py    # SQLite persistence layer
├── data/
│   └── documents/       # Indexed medical records
├── app.py               # Main Streamlit Dashboard
└── requirements.txt     # System dependencies
```

## 🛠️ Installation & Setup

1. **Clone & Install**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment Configuration**:
   Create a `.env` file in the root:
   ```
   GROQ_API_KEY=your_key_here
   ```
3. **Launch Dashboard**:
   ```bash
   streamlit run app.py
   ```

## 📋 Best Practices
- **Medical Records**: Upload clinical PDFs in the sidebar for personalized analysis.
- **Emergencies**: Any mention of chest pain or acute symptoms will trigger the Emergency Guard.
- **Analytics**: Visit the Analytics tab to see a registry of all scheduled consultations.

---
*Disclaimer: MediGuide AI provides informational guidance only and is not a clinical surrogate. For life-threatening emergencies, always call 911 or visit the nearest ER.*
