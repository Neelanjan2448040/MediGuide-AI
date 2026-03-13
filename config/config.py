import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Safely get the API key from Streamlit Cloud Secrets or local .env
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DATABASE_PATH = "database/mediguide.db"
FAISS_INDEX_PATH = "database/faiss_index"
DATA_DIR = "data/documents"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs("database", exist_ok=True)
