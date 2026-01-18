
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import get_settings
from src.core.ssl_handler import configure_ssl_handling

configure_ssl_handling()
settings = get_settings()
os.environ["GOOGLE_API_KEY"] = settings.google_api_key

models = ["models/text-embedding-004", "text-embedding-004", "models/embedding-001"]

for m in models:
    print(f"Testing Embedding: {m}")
    try:
        emb = GoogleGenerativeAIEmbeddings(model=m)
        vec = emb.embed_query("hello")
        print(f"[OK] Success! Vector len: {len(vec)}")
        break
    except Exception as e:
        print(f"[X] Failed: {e}")
