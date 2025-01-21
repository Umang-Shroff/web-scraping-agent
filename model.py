import os
from pydantic_ai.models.gemini import GeminiModel
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    raise ValueError("API key is not set. Please check your .env file.")

try:
    GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp', api_key=api_key)
    print("Model is successfully.")
except Exception as e:
    print(f"Error loading the model: {e}")
    raise
