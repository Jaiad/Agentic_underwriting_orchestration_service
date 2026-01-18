
"""
Advanced LangChain Orchestrator
-------------------------------
This file demonstrates how to replace the specific regex/logic portions of the 
original orchestrator with modern LangChain components.

KEY CONCEPTS DEMONSTRATED:
1.  **LCEL (LangChain Expression Language)**: Using `|` to compose chains.
2.  **PydanticOutputParser**: Enforcing structured JSON output from the LLM.
3.  **PromptTemplates**: separating instruction logic from dynamic inputs.
4.  **ChatGoogleGenerativeAI**: Using the real Gemini model.

Usage:
    Ensure GOOGLE_API_KEY is in your .env file.
    Run: python langchain_orchestrator_advanced.py
"""

import os
import sys
import warnings
import urllib3
import requests

# ==========================================
# SSL PATCH (For Development/Proxy Envs)
# ==========================================
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'

# Monkey patch requests to ignore SSL globally
old_merge_environment_settings = requests.Session.merge_environment_settings
def new_merge_environment_settings(self, url, proxies, stream, verify, cert):
    return old_merge_environment_settings(self, url, proxies, stream, False, cert)
requests.Session.merge_environment_settings = new_merge_environment_settings

from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# LangChain Imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# ==========================================
# CONCEPT 1: Pydantic Models for Schema
# ==========================================
# Instead of guessing dictionary keys, we define exactly what we want.
class InsuranceExtraction(BaseModel):
    client_name: str = Field(description="Name of the company or person requesting the quote")
    industry_type: str = Field(description="Classify into one of: 'Current', 'Construction', 'Restaurant', 'Retail', 'Technology', 'Other'")
    revenue_annual: int = Field(description="Annual revenue in USD found in the text. Convert '15M' to 15000000.")
    employee_count: Optional[int] = Field(description="Number of employees if mentioned, else 0")
    requested_coverages: List[str] = Field(description="List of insurance types requested (e.g. 'General Liability', 'Auto')")

class AdvancedOrchestrator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ ERROR: GOOGLE_API_KEY not found in .env")
            print("Please add your key to run this advanced version.")
            self.model = None
            return

        # ==========================================
        # CONCEPT 2: Chat Model Initialization
        # ==========================================
        # We treat the model as a 'Runnable' component.
        try:
            self.model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=api_key,
                temperature=0  # Low temperature for factual extraction
            )
        except Exception as e:
            print(f"Error initializing model: {e}")
            self.model = None

        # ==========================================
        # CONCEPT 3: Setting up the Parser
        # ==========================================
        self.parser = PydanticOutputParser(pydantic_object=InsuranceExtraction)

        # ==========================================
        # CONCEPT 4: Prompt Templates
        # ==========================================
        # We inject {format_instructions} to tell the LLM how to format the JSON.
        self.extract_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert AI underwriter. Your job is to extract precise data options."),
            ("human", """Extract the following information from the email.
            
            EMAIL CONTENT:
            {email}
            
            {format_instructions}
            """)
        ])

        # ==========================================
        # CONCEPT 5: LCEL (LangChain Expression Language)
        # ==========================================
        # The syntax `Step1 | Step2 | Step3` creates a Chain.
        if self.model:
            self.extraction_chain = (
                self.extract_prompt 
                | self.model 
                | self.parser
            )
            
            # A second simple chain for generating the response letter
            self.letter_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful insurance agent."),
                ("human", "Write a professional quote email for {client_name} in {industry}. The total premium is ${premium:,}.")
            ])
            
            self.letter_chain = self.letter_prompt | self.model | StrOutputParser()

    def process_quote(self, email_content: str):
        if not self.model:
            print("Skipping process: Model not initialized.")
            return

        print("\n--- 🧠 STEP 1: Running Extraction Chain (LCEL) ---")
        try:
            # We invoke the chain. Notice we pass 'format_instructions' automatically via the parser.
            data: InsuranceExtraction = self.extraction_chain.invoke({
                "email": email_content,
                "format_instructions": self.parser.get_format_instructions()
            })
            
            print("✅ Extraction Successful!")
            print(f"   Matches Schema: {isinstance(data, InsuranceExtraction)}")
            print(f"   Client: {data.client_name}")
            print(f"   Industry: {data.industry_type}")
            print(f"   Revenue: ${data.revenue_annual:,.2f}")
            
        except Exception as e:
            print(f"❌ Extraction Chain Failed: {e}")
            return

        # (Simulating the Logic/Calculation Step - usually pure Python)
        print("\n--- 🧮 STEP 2: Calculating Premium (Business Logic) ---")
        base_rate = 0.005 if data.industry_type == 'Technology' else 0.02
        premium = data.revenue_annual * base_rate
        print(f"   Calculated Premium: ${premium:,.2f}")

        print("\n--- ✍️ STEP 3: Generating Response Letter (LCEL) ---")
        try:
            letter = self.letter_chain.invoke({
                "client_name": data.client_name,
                "industry": data.industry_type,
                "premium": premium
            })
            print("\n" + letter)
        except Exception as e:
            print(f"❌ Generation Failed: {e}")

# ==========================================
# Execution Demo
# ==========================================
if __name__ == "__main__":
    print("Initializing Advanced Orchestrator...")
    orchestrator = AdvancedOrchestrator()
    
    sample_email = """
    Subject: Quote for TechStartup Inc
    
    Hello,
    We are a small SaaS company called TechStartup Inc.
    We are looking for cyber liability and standard GL.
    Our annual revenue is roughly $5,000,000 and we have 12 employees.
    Please send a quote.
    """
    
    orchestrator.process_quote(sample_email)
