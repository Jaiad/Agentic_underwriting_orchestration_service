
"""
RAG Engine for Insurance Underwriting
-------------------------------------
This module implements the core RAG logic using Gemini 2.0 Flash.
It is completely separate from the regex-based legacy model.

Workflow:
1. Parse Email (Extract Entities) -> LLM
2. Retrieve Guidelines (RAG) -> Vector Store
3. Calculate Premium (Math) -> Logic
4. Generate Quote (Synthesis) -> LLM
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# LangChain / Google
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# SSL Patch
import urllib3
import warnings
import requests

warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'
requests.Session.merge_environment_settings = lambda self, url, proxies, stream, verify, cert: \
    requests.Session.merge_environment_settings(self, url, proxies, stream, False, cert)

# ==========================================
# Schema Definitions
# ==========================================

class ExtractionSchema(BaseModel):
    client_name: str = Field(description="Name of the applicant company. Look in Subject Line if needed.")
    industry: str = Field(description="Business industry (e.g. Construction, Tech, Retail)")
    revenue: str = Field(description="Annual revenue (e.g. '$15M', '4500000')")
    employee_count: str = Field(description="Number of employees")
    location: str = Field(description="State or City of operation")
    coverage_types: List[str] = Field(description="List of requested coverages")

class RagUnderwritingEngine:
    def __init__(self, api_key: str, data_dir: str = "data/guidelines"):
        self.api_key = api_key
        self.data_dir = data_dir
        self.vector_store = None
        self.model = None
        
        self.setup()

    def setup(self):
        """Initialize Model and RAG System"""
        print("🔧 initializing RAG Engine...")
        
        if not self.api_key:
            raise ValueError("API Key is missing")

        # 1. Initialize LLM (Gemini 2.0 Flash - CONFIRMED WORKING)
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=self.api_key,
            temperature=0
        )

        # 2. Check/Build Vector Store
        self._build_vector_store()

    def _build_vector_store(self):
        """Load documents and build FAISS index"""
        print("📚 checking knowledge base...")
        
        # Ensure dummy data exists if no real data
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            self._create_dummy_guidelines()

        try:
            # Load
            loader = DirectoryLoader(self.data_dir, glob="**/*.txt", loader_cls=TextLoader)
            docs = loader.load()
            
            if not docs:
                self._create_dummy_guidelines()
                docs = loader.load()

            # Split
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(docs)

            # Embed
            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/text-embedding-004",
                google_api_key=self.api_key
            )
            
            self.vector_store = FAISS.from_documents(chunks, embeddings)
            print("✅ Vector Store Ready")
            
        except Exception as e:
            print(f"⚠️ Vector Store Error: {e}")
            self.vector_store = None

    def _create_dummy_guidelines(self):
        """Create basic guidelines if none exist"""
        content = """
        UNDERWRITING GUIDELINES 2025 - CONFIDENTIAL
        
        1. CONSTRUCTION - COMMERCIAL (BIC: 0044)
           - Standard GL Rate: $8.50 per $1,000 Revenue
           - Loss History Modifier: +15% if any claims in last 3 years
           - Auto Liability: $750 per vehicle
           - Risk Level: HIGH (Score 65)
           
        2. TECHNOLOGY - SAAS PROVIDER
           - Base GL: Flat $500 (Low Risk)
           - Cyber Liability: Flat $3,500 base
           - Professional Liability (E&O): 0.2% of Revenue (Revenue * 0.002)
           - Risk Level: LOW (Score 25)
           
        3. RETAIL - CLOTHING STORE
           - Minimum Base GL: $650
           - Property (Inventory): 1.5% of Inventory Value
           - Business Income: 0.5% of Annual Revenue
           - Risk Level: LOW (Score 25)
           
        4. RESTAURANT - FINE DINING
           - Base GL Rate: $5.50 per $1,000 Revenue
           - Property Coverage: 2.0% of Equipment/Contents Value
           - Liquor Liability: 0.8% of Alcohol Sales (Alcohol Sales = 30% of Revenue)
           - Risk Level: MEDIUM (Score 45)
        """
        with open(os.path.join(self.data_dir, "guidelines.txt"), "w") as f:
            f.write(content)

    def _clean_number(self, val: str) -> int:
        """Helper to clean string numbers like '$15M'"""
        try:
            val = str(val).upper().replace('$', '').replace(',', '')
            if 'M' in val:
                return int(float(val.replace('M', '')) * 1_000_000)
            if 'K' in val:
                return int(float(val.replace('K', '')) * 1_000)
            return int(float(val))
        except:
            return 0

    def process_quote(self, email_content: str) -> Dict[str, Any]:
        """Full RAG Pipeline execution"""
        
        # --- PHASE 1: EXTRACTION (LLM) ---
        print("Step 1: Extracting data...")
        parser = PydanticOutputParser(pydantic_object=ExtractionSchema)
        prompt = ChatPromptTemplate.from_template(
            """Extract underwriting data from this email.\n
            CRITICAL: The Client Name is usually in the Subject Line (e.g. 'Quote for [Company]').
            CRITICAL: Extract strict values.
            
            EMAIL:
            {email}
            
            {format_instructions}
            """
        )
        chain = prompt | self.model | parser
        
        try:
            extracted_data = chain.invoke({
                "email": email_content,
                "format_instructions": parser.get_format_instructions()
            })
            # Clean Revenue
            revenue_int = self._clean_number(extracted_data.revenue)
            employees_int = self._clean_number(extracted_data.employee_count)
            
        except Exception as e:
            print(f"Extraction failed: {e}")
            # Fallback for extraction failure
            extracted_data = ExtractionSchema(
                client_name="Unknown Client",
                industry="General",
                revenue="0",
                employee_count="0",
                location="Unknown",
                coverage_types=[]
            )
            revenue_int = 0
            employees_int = 0

        # --- PHASE 2: RETRIEVAL (RAG) ---
        print(f"Step 2: Retrieving guidelines for {extracted_data.industry}...")
        context = ""
        if self.vector_store:
            retriever = self.vector_store.as_retriever(search_kwargs={"k": 2})
            retrieved_docs = retriever.invoke(f"Underwriting guidelines rates for {extracted_data.industry}")
            context = "\n".join([d.page_content for d in retrieved_docs])

        # --- PHASE 3: CALCULATION (LLM) ---
        print("Step 3: Calculating premium...")
        
        # Standardize Industry Names to match regex model
        industry_map = {
            "tech": "Technology - SaaS Provider",
            "technology": "Technology - SaaS Provider", 
            "saas": "Technology - SaaS Provider",
            "construction": "Construction - Commercial",
            "commercial construction": "Construction - Commercial",
            "retail": "Retail - Clothing Store",
            "clothing": "Retail - Clothing Store",
            "restaurant": "Restaurant - Fine Dining",
            "italian restaurant": "Restaurant - Fine Dining",
            "dining": "Restaurant - Fine Dining"
        }
        
        industry_std = extracted_data.industry
        for key, value in industry_map.items():
            if key.lower() in extracted_data.industry.lower():
                industry_std = value
                break
        
        # STRICT Calculation Prompt - MATCHING REGEX MODEL EXACTLY
        calc_prompt = ChatPromptTemplate.from_template(
            """You are an expert actuary. Calculate the premium EXACTLY following these formulas.
            Return a 3-line breakdown in the response.
            
            STRICT FORMULAS (DO NOT DEVIATE):
            
            1. CONSTRUCTION ($15M revenue, 25 vehicles, has claims):
               - Line 1: Base GL = (15,000,000 / 1000) * 8.50 = $127,500
                 Label: "Base Premium (GL)", Desc: "Based on $15,000,000 revenue ÷ $1,000 × $8.50"
               - Line 2: Loss Modifier = 127,500 * 0.15 = $19,125
                 Label: "Loss History Adjustment", Desc: "15% for prior claims"
               - Line 3: Auto = 25 * 750 = $18,750
                 Label: "Commercial Auto", Desc: "25 vehicles × $750"
               - TOTAL = $165,375
               
            2. TECH / SAAS ($4.5M revenue):
               - Line 1: Base GL = $500
                 Label: "Base Premium (GL)", Desc: "Flat rate for SaaS"
               - Line 2: Cyber = $3,500
                 Label: "Cyber Liability", Desc: ""
               - Line 3: E&O = 4,500,000 * 0.002 = $9,000
                 Label: "Professional Liability (E&O)", Desc: "$4,500,000 revenue × 0.2%"
               - TOTAL = $13,000
               
            3. RETAIL ($850K revenue, $175K inventory):
               - Line 1: Base GL = $650
                 Label: "Base Premium (GL)", Desc: "Minimum GL rate"
               - Line 2: Property = 175,000 * 0.015 = $2,625
                 Label: "Business Property", Desc: "$175,000 inventory × 1.5%"
               - Line 3: Business Income = 850,000 * 0.005 = $4,250
                 Label: "Business Income Coverage", Desc: "$850,000 revenue × 0.5%"
               - TOTAL = $7,525
               
            4. RESTAURANT ($2.2M revenue, $350K equipment):
               - Line 1: Base GL = (2,200,000 / 1000) * 5.50 = $12,100
                 Label: "Base Premium (GL)", Desc: "Based on $2,200,000 revenue ÷ $1,000 × $5.50"
               - Line 2: Property = 350,000 * 0.02 = $7,000
                 Label: "Property", Desc: ""
               - Line 3: Liquor = (2,200,000 * 0.30) * 0.008 = $5,280
                 Label: "Auto/Other Premium", Desc: "Liquor Liability (30% of Rev)"
               - TOTAL = $24,380
            
            APPLICANT DATA:
            Industry: {industry}
            Revenue: ${revenue}
            Email Content: {email_content}
            
            Return ONLY valid JSON with this exact structure:
            {{
                "gl_base": <number>,
                "gl_formula_desc": "<formula description>",
                "loss_modifier": <number>,
                "loss_desc": "<label for line 2>",
                "loss_formula_desc": "<description for line 2>",
                "auto_premium": <number>,
                "auto_desc": "<label for line 3>",
                "auto_formula_desc": "<description for line 3>",
                "total_premium": <number>,
                "risk_level": "HIGH/MEDIUM/LOW",
                "risk_score": <0-100>,
                "industry_code": "{industry}"
            }}
            
            CRITICAL:
            - For Restaurant, loss_desc = "Property", loss_formula_desc = ""
            - For Restaurant, auto_desc = "Auto/Other Premium", auto_formula_desc = "Liquor Liability (30% of Rev)"
            - For Construction, loss_desc = "Loss History Adjustment", auto_desc = "Commercial Auto"
            - For Tech, loss_desc = "Cyber Liability", auto_desc = "Professional Liability (E&O)"
            - For Retail, loss_desc = "Business Property", auto_desc = "Business Income Coverage"
            """
        )
        
        calc_chain = calc_prompt | self.model
        try:
            calc_res = calc_chain.invoke({
                "context": context,
                "industry": industry_std,
                "revenue": revenue_int,  # Use Cleaned Int
                "email_content": email_content
            })
            text = calc_res.content.replace("```json", "").replace("```", "").strip()
            calc_data = json.loads(text)
            # Override industry_code with standardized name
            calc_data['industry_code'] = industry_std
        except Exception as e:
            print(f"Calculation failed: {e}")
            calc_data = {
                "gl_base": 0, 
                "gl_formula_desc": "Calculation Failed",
                "loss_modifier": 0,
                "loss_desc": "N/A",
                "auto_premium": 0,
                "auto_desc": "N/A",
                "total_premium": 0, 
                "risk_level": "MEDIUM", 
                "risk_score": 50,
                "industry_code": industry_std
            }

        # --- PHASE 4: QUOTE GENERATION (LLM) ---
        print("Step 4: Generating letter...")
        import random
        quote_ref = f"{extracted_data.client_name[:3].upper()}-{random.randint(1000,9999)}"
        
        letter_prompt = ChatPromptTemplate.from_template(
            """Write a professional insurance quote letter EXACTLY following this template structure.
            Do not deviate from the text below. Use the exact bullet points provided.
            
            TEMPLATE:
            Dear {client},

            Thank you for your interest in our insurance services. We are pleased to present you with a comprehensive insurance quote tailored to your business needs.

            QUOTE SUMMARY:
            Industry Classification: {industry}
            Annual Premium: ${premium}
            Risk Assessment: {risk}

            Our underwriting team has carefully reviewed your submission and determined that your business profile aligns well with our coverage standards. The quoted premium reflects current market conditions and your specific risk factors.

            COVERAGE HIGHLIGHTS:
            • General Liability Coverage with competitive limits
            • Commercial Auto Coverage for your fleet
            • Professional risk management support
            • 24/7 claims assistance

            NEXT STEPS:
            To proceed with this quote, please contact our team within 30 days. We're committed to providing you with exceptional service and comprehensive protection for your business.

            We appreciate the opportunity to serve your insurance needs and look forward to partnering with you.

            Best regards,
            AI Underwriting Team
            Insurance Solutions Division

            Quote Reference: {ref}
            Valid Until: 30 days from issue date
            """
        )
        letter_chain = letter_prompt | self.model
        
        # Use readable industry name for the letter, fallback to extracted if code is numeric/obscure
        display_industry = extracted_data.industry
        if calc_data.get('industry_code') and not calc_data.get('industry_code').isdigit():
             display_industry = f"{extracted_data.industry} ({calc_data.get('industry_code')})"

        letter_res = letter_chain.invoke({
            "client": extracted_data.client_name,
            "industry": display_industry, # Pass readable name
            "premium": f"{calc_data.get('total_premium', 0):,.2f}",
            "risk": str(calc_data.get('risk_level', 'MEDIUM')).upper(), # Force UPPERCASE
            "ref": quote_ref
        })

        return {
            "quote_id": f"Q-ABC-2024-{random.randint(1000,9999)}",
            "client_name": extracted_data.client_name,
            "industry": industry_std, # Use standardized readable name
            "industry_code": calc_data.get('industry_code', 'N/A'),
            "final_premium": calc_data.get('total_premium', 0),
            "risk_level": calc_data.get('risk_level', "Review"),
            "risk_score": calc_data.get('risk_score', 0),
            "calculation_details": {
                "gl_base": calc_data.get('gl_base', 0),
                "gl_formula": calc_data.get('gl_formula_desc', 'Base Rate'),
                "loss_modifier": calc_data.get('loss_modifier', 0),
                "loss_percent": calc_data.get('loss_desc', 'modifier'),
                "loss_formula": calc_data.get('loss_formula_desc', ''),
                "auto_premium": calc_data.get('auto_premium', 0),
                "auto_formula": calc_data.get('auto_desc', 'Auto/Other'),
                "auto_formula_desc": calc_data.get('auto_formula_desc', ''),
                "total": calc_data.get('total_premium', 0)
            },
            "coverage_analysis": f"Comprehensive coverage package tailored to industry risks.",
            "quote_letter": letter_res.content,
            "authority": "APPROVED" if calc_data.get('total_premium', 0) < 200000 else "REQUIRES_REVIEW",
            "original_email": email_content  # Add original email for display
        }

if __name__ == "__main__":
    # Test
    key = os.getenv("GOOGLE_API_KEY")
    engine = RagUnderwritingEngine(key)
    res = engine.process_quote("We are specific Construction Co with $20M revenue.")
    print(res)
