import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Safely get the API key from Streamlit Cloud Secrets or local .env
GROQ_API_KEY = None
try:
    if "GROQ_API_KEY" in st.secrets:
        GROQ_API_KEY = str(st.secrets["GROQ_API_KEY"]).strip()
except Exception:
    pass

if not GROQ_API_KEY:
    val = os.getenv("GROQ_API_KEY")
    if val:
        GROQ_API_KEY = val.strip()

DATABASE_PATH = "database/mediguide.db"
FAISS_INDEX_PATH = "database/faiss_index"
DATA_DIR = "data/documents"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs("database", exist_ok=True)
