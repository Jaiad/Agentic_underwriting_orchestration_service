
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import get_settings
from src.core.ssl_handler import configure_ssl_handling

configure_ssl_handling()

# Load settings to get key
settings = get_settings()
os.environ["GOOGLE_API_KEY"] = settings.google_api_key

print(f"Testing with Key: {settings.google_api_key[:10]}...")

models_to_test = [
    "gemini-1.5-flash",
    "models/gemini-1.5-flash",
    "gemini-pro",
    "models/gemini-pro",
    "gemini-1.5-pro",
    "models/gemini-1.5-pro",
    "gemini-2.0-flash-exp", # Sometimes available
]

for model_name in models_to_test:
    print(f"\n--- Testing Model: {model_name} ---")
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            convert_system_message_to_human=True
        )
        res = llm.invoke("Say 'Success'")
        print(f"[OK] SUCCESS! Output: {res.content}")
        print(f"USE THIS MODEL: {model_name}")
        break  # Stop after first success
    except Exception as e:
        print(f"[X] Failed: {e}")
