from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY

def get_llm(model_name="llama-3.3-70b-versatile", temperature=0.7):
    """
    Returns a Groq LLM instance.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    
    return ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=model_name,
        temperature=temperature
    )
