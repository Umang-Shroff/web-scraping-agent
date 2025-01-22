import os
from pydantic_ai.models.gemini import GeminiModel
import streamlit as st

# Access the GEMINI_API_KEY stored in secrets (from Streamlit and not dotenv)
api_key = st.secrets["GEMINI_API_KEY"]

# for getting api key from .env file
# load_dotenv()
# api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    raise ValueError("API key is not set. Please check your secrets.toml file.")

try:
    GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp', api_key=api_key)
    print("Model is successfully loaded.")
except Exception as e:
    print(f"Error loading the model: {e}")
    raise
