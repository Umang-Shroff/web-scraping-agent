import os
from pydantic_ai.models.gemini import GeminiModel  

try:
    GEMINI_MODEL = GeminiModel('gemini-2.0-flash-exp')
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading the model: {e}")
