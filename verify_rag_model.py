
"""
Verification Script for RAG Engine
----------------------------------
Tests the RAG Pipeline logic without the web server.
"""

import sys
import os
import asyncio

sys.path.append(os.getcwd())
from src.rag_source.rag_engine import RagUnderwritingEngine

def test_rag_quote():
    print("--- 🧪 Starting Verification ---")
    
    key = os.getenv("GOOGLE_API_KEY", "AIzaSyAMNfmzMDjUl4XncYBF2yEu_xvtJ-zkLzo")
    engine = RagUnderwritingEngine(key, data_dir="data/guidelines")
    
    # Test Payload
    test_email = """
    Subject: Quote for VerifyTech
    
    Hi,
    We are VerifyTech, a SaaS company in California.
    Revenue is $2,000,000.
    We have 10 employees.
    Looking for standard coverage.
    """
    
    print("\n[Input Email]:")
    print(test_email.strip())
    
    print("\n[Processing]...")
    result = engine.process_quote(test_email)
    
    print("\n--- ✅ Result ---")
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
        
    print(f"Client: {result.get('client_name')}")
    print(f"Premium: {result.get('final_premium')}")
    print(f"Letter Length: {len(result.get('quote_letter', ''))}")
    
    # Assertions
    if result.get('final_premium') > 0 and result.get('client_name'):
        print("\nPASSED: Output structure is valid.")
    else:
        print("\nFAILED: Invalid output structure.")

if __name__ == "__main__":
    test_rag_quote()
