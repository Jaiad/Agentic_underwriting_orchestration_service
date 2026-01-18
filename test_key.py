
import os
import google.generativeai as genai
from src.config import get_settings
from src.core.ssl_handler import configure_ssl_handling

configure_ssl_handling()

def test_key():
    try:
        settings = get_settings()
        key = settings.google_api_key
        print(f"Testing Key: {key[:10]}...")
        
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_key()
