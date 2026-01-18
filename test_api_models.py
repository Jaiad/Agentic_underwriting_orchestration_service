
import os
import sys
import warnings
import urllib3
import requests
import google.generativeai as genai
from colorama import init, Fore, Style

# --- SSL ERROR PATCH ---
# This fixes "CERTIFICATE_VERIFY_FAILED" on corporate networks/proxies
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'

# Monkey patch requests
old_merge_environment_settings = requests.Session.merge_environment_settings
def new_merge_environment_settings(self, url, proxies, stream, verify, cert):
    return old_merge_environment_settings(self, url, proxies, stream, False, cert)
requests.Session.merge_environment_settings = new_merge_environment_settings
# -----------------------

init()

def test_google_models():
    print(f"\n{Fore.CYAN}=== Testing Google Gemini Models ==={Style.RESET_ALL}")
    
    api_key = "AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo"
    if not api_key:
        print(f"{Fore.RED}No GOOGLE_API_KEY found!{Style.RESET_ALL}")
        return

    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    
    # Configure GenAI
    genai.configure(api_key=api_key)

    # List of models to test
    candidates = [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "gemini-1.0-pro"
    ]

    working_model = None

    for model_name in candidates:
        print(f"\nTesting model: {Fore.YELLOW}{model_name}{Style.RESET_ALL}...", end=" ")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Test Successful'")
            if response and response.text:
                print(f"{Fore.GREEN}✅ WORKING{Style.RESET_ALL}")
                print(f"   Output: {response.text.strip()}")
                if not working_model:
                    working_model = model_name
            else:
                print(f"{Fore.RED}❌ EMPTY RESPONSE{Style.RESET_ALL}")
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print(f"{Fore.RED}❌ NOT FOUND (404){Style.RESET_ALL}")
            elif "403" in error_msg or "PERMISSION_DENIED" in error_msg:
                print(f"{Fore.RED}❌ PERMISSION DENIED{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ ERROR: {str(e)[:100]}...{Style.RESET_ALL}")

    return working_model

if __name__ == "__main__":
    print(f"{Fore.WHITE}Starting API & Model Diagnostic...{Style.RESET_ALL}")
    
    best_google = test_google_models()
    
    print(f"\n{Fore.CYAN}=== DIAGNOSTIC SUMMARY ==={Style.RESET_ALL}")
    if best_google:
        print(f"Recommended Google Model: {Fore.GREEN}{best_google}{Style.RESET_ALL}")
        print(f"Update your code to use: model='{best_google}'")
    else:
        print(f"{Fore.RED}No working Google models found with provided key.{Style.RESET_ALL}")
