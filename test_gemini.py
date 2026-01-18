import google.generativeai as genai
import os
import ssl
import warnings
import urllib3

# SSL Patch from fireworks_client.py
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'
import requests
# Monkey patch requests to ignore SSL globally
old_merge_environment_settings = requests.Session.merge_environment_settings
def new_merge_environment_settings(self, url, proxies, stream, verify, cert):
    # Always set verify to False
    return old_merge_environment_settings(self, url, proxies, stream, False, cert)
requests.Session.merge_environment_settings = new_merge_environment_settings

api_key = "AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo"
print(f"Testing with key: {api_key[:5]}...")

genai.configure(api_key=api_key, transport='rest')

print("--- Testing models/gemini-1.5-pro ---")
try:
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    response = model.generate_content("Hello")
    print("Success:", response.text)
except Exception as e:
    print("Failed:", e)

print("\n--- Testing gemini-1.5-pro ---")
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content("Hello")
    print("Success:", response.text)
except Exception as e:
    print("Failed:", e)
