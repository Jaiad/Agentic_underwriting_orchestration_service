
import google.generativeai as genai
import os
import ssl

# Basic SSL patch
try:
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context
except AttributeError:
    pass

key = "AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo"
print(f"Using key: {key[:5]}...")
genai.configure(api_key=key)

try:
    print("Listing models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    print("List complete.")
    
    print("Testing generation...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    res = model.generate_content("Hi")
    print(f"Generation success: {res.text}")

except Exception as e:
    print(f"Error: {e}")
