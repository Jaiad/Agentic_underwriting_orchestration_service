from openai import OpenAI
import os

api_key = "MjgyMzc1a2ZjZ29hNzc4NWUwMTcxMjRncjk6MzgyMjgxNmUtZTc3My00OTdhLWIyYTQtODYyNWUxYmNlNjJk"
base_url = "https://integrate.api.nvidia.com/v1"

client = OpenAI(base_url=base_url, api_key=api_key)

try:
    models = [m.id for m in client.models.list().data]
    print(f"Found {len(models)} models.")
except Exception as e:
    print(f"List failed: {e}")
    models = []

# Prioritize Llama
priority_models = [m for m in models if "llama-3.1-70b" in m.lower() and "meta" in m.lower()]
if not priority_models:
    priority_models = [m for m in models if "llama-3.1" in m.lower()]
if not priority_models:
    priority_models = models[:5] # Fallback to first 5

print(f"Testing models: {priority_models}")

for model in priority_models:
    print(f"Testing {model}...")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print(f"SUCCESS with {model}: {response.choices[0].message.content}")
        break
    except Exception as e:
        print(f"FAILED {model}: {e}")
