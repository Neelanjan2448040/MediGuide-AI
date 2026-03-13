import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_PATH = "database/mediguide.db"
FAISS_INDEX_PATH = "database/faiss_index"
DATA_DIR = "data/documents"

# Create directories if they don't exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs("database", exist_ok=True)
