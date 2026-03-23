import os
from google import genai
from google.genai import types

def create_gemini_client() -> genai.Client:
    """geminiのクライアントを作成する"""
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=gemini_api_key)
    return client
