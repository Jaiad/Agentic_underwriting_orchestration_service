"""
Direct REST Client for Google Gemini (Bypassing Library Issues).
"""

import json
import os
import requests
import warnings
import urllib3
from functools import lru_cache
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import get_settings

# --- SSL Aggressive Patch ---
# If inside corporate network, proxies might be intercepting
# Force unset proxies for this specific request if needed
os.environ['NO_PROXY'] = 'generativelanguage.googleapis.com'

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Monkey patch requests to ignore SSL globally
_original_merge_environment_settings = requests.Session.merge_environment_settings
def _patched_merge_environment_settings(self, url, proxies, stream, verify, cert):
    # Ignoring the 'verify' argument and forcing False
    # Also verify if proxies are being picked up
    return _original_merge_environment_settings(self, url, proxies, stream, False, cert)
requests.Session.merge_environment_settings = _patched_merge_environment_settings


class FireworksClient:
    """
    Direct REST client for Google Gemini API.
    """

    def __init__(self):
        settings = get_settings()
        self.api_key = settings.google_api_key or settings.fireworks_api_key
        if not self.api_key:
             raise ValueError("API Key missing")
             
        self.llm_model = "gemini-2.0-flash-exp"
        self.embedding_model = "text-embedding-004"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:
        url = f"{self.base_url}/models/{self.llm_model}:generateContent?key={self.api_key}"
        
        contents = []
        if system_prompt:
             contents.append({"role": "user", "parts": [{"text": system_prompt}]})
             contents.append({"role": "model", "parts": [{"text": "Understood."}]})
        
        contents.append({"role": "user", "parts": [{"text": prompt}]})
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        
        try:
             text_data = response.text
             print(f"DEBUG RESPONSE TEXT: {text_data[:500]}")
             data = response.json()
             return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            print(f"Gemini API Error Response: {data}")
            print(f"Exception: {e}")
            return ""

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_json(
        self,
        prompt: str,
        schema: Optional[Type[BaseModel]] = None,
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        
        full_system = "You must respond with valid JSON only."
        if system_prompt:
            full_system = f"{system_prompt}\n\n{full_system}"
            
        if schema:
            schema_json = json.dumps(schema.model_json_schema(), indent=2)
            prompt = f"{prompt}\n\nRespond with JSON matching this schema:\n{schema_json}"
            
        text_response = self.generate(prompt, full_system, temperature, max_tokens)
        
        # Parse JSON
        text = text_response.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {text[:200]}...")
            # Try to partial parse or return empty dict
            return {}

    def generate_embeddings(
        self,
        texts: List[str],
        prefix: str = ""
    ) -> List[List[float]]:
        # Batch embedding
        url = f"{self.base_url}/models/{self.embedding_model}:batchEmbedContents?key={self.api_key}"
        
        requests_data = []
        for text in texts:
             content = text
             if prefix:
                  content = f"{prefix}{text}"
             requests_data.append({
                 "model": f"models/{self.embedding_model}",
                 "content": {"parts": [{"text": content}]},
                 "taskType": "RETRIEVAL_DOCUMENT"
             })
             
        payload = {"requests": requests_data}
        
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            data = response.json()
            return [start.get("values", []) for start in [e.get("embedding", {}) for e in data.get("embeddings", [])]]
        except Exception as e:
            print(f"Embedding failed: {e}")
            return [[0.0] * 768 for _ in texts]

    def generate_embedding(self, text: str, prefix: str = "") -> List[float]:
        # Single embedding
        url = f"{self.base_url}/models/{self.embedding_model}:embedContent?key={self.api_key}"
        
        content = text
        if prefix:
              content = f"{prefix}{text}"
              
        payload = {
            "model": f"models/{self.embedding_model}",
            "content": {"parts": [{"text": content}]},
            "taskType": "RETRIEVAL_DOCUMENT"
        }
        
        try:
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            data = response.json()
            return data["embedding"]["values"]
        except Exception as e:
            print(f"Embedding failed: {e}")
            return [0.0] * 768

@lru_cache()
def get_fireworks_client() -> FireworksClient:
    return FireworksClient()
