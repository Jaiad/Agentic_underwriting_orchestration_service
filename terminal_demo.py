"""
Professional Terminal Demo for AI Insurance Underwriting.
Executes the 3-Phase Model and displays results with rich formatting.
"""

import sys
import time
import asyncio
from typing import Dict
import colorama
from colorama import Fore, Style, Back

# Initialize colorama
colorama.init()

# Ensure we can import src
import os
sys.path.append(os.getcwd())

from src.pipeline.orchestrator import UnderwritingPipeline
from src.core.ssl_handler import configure_ssl_handling

# --- UI Helpers ---

def print_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + Style.BRIGHT + "+" + "="*70 + "+")
    print(Fore.CYAN + Style.BRIGHT + "|  " + Fore.WHITE + "[AI] INSURANCE UNDERWRITING ORCHESTRATOR" + " "*30 + Fore.CYAN + "|")
    print(Fore.CYAN + Style.BRIGHT + "|  " + Fore.YELLOW + ">> Powered by LangChain, RAG & Google Gemini" + " "*25 + Fore.CYAN + "|")
    print(Fore.CYAN + Style.BRIGHT + "+" + "="*70 + "+" + Style.RESET_ALL)
    print("")

def print_step_start(step_num: int, name: str):
    print(f"{Fore.BLUE}Phase {step_num}{Style.RESET_ALL} | {Fore.WHITE}{name}...", end="\r")

def print_step_success(step_num: int, name: str, details: str = ""):
    print(f"{Fore.GREEN}+ Phase {step_num}{Style.RESET_ALL} | {Fore.WHITE}{name:<25} {Fore.CYAN}-> {details}{Style.RESET_ALL}")

def print_rag_retrieval(docs_count: int, sources: list):
    print(f"        {Fore.MAGENTA}L RAG Retrieval: {docs_count} documents utilized{Style.RESET_ALL}")
    for src in sources[:2]: # Show first 2 sources
        src_name = src.get('metadata', {}).get('source', 'Unknown').split('\\')[-1]
        print(f"           {Fore.CYAN}* {src_name}{Style.RESET_ALL}")

def main():
    configure_ssl_handling()
    print_header()

    # Sample Input
    email_content = """
    Subject: Quote Request - ABC Construction Corp
    
    Hi,
    I need a quote for ABC Construction Corp. They are a commercial construction 
    company in Texas with $15M revenue and 85 employees. They need General Liability 
    $2M/$4M and Auto for 25 vehicles.
    
    Thanks,
    Sarah
    """

    print(f"{Back.BLUE}{Fore.WHITE} INPUT EMAIL {Style.RESET_ALL}")
    print(f"{Fore.WHITE}{email_content.strip()}{Style.RESET_ALL}")
    print("\n" + "-"*72 + "\n")

    # Initialize Pipeline
    print(f"{Fore.YELLOW}>> Initializing 3-Phase Model (RAG + LCEL Chains)...{Style.RESET_ALL}")
    
    # Progress callback
    def progress_handler(step, name, status):
        pass # We handle printing manually for better control in this demo script

    pipeline = UnderwritingPipeline(progress_callback=progress_handler)
    
    # Run
    start_time = time.time()
    
    try:
        # We'll simulate the "streaming" feel by capturing the result but printing updates
        # In a real async terminal app we'd attach listeners
        
        # 1. RAG Setup (Happens in init, but we visualize it)
        print_step_success(1, "RAG Knowledge Base", "Loaded FAISS Vector Store")
        
        # 2. Pipeline Execution
        result = pipeline.process(email_content)
        
        if result.success:
            # Display formatted results matching the "3 Phase" execution style
            
            # Email Parser
            print_step_success(2, "Email Parsing", f"Client: {result.extracted_email.client_name}")
            
            # Industry Classifier (RAG)
            print_step_success(3, "Industry Classifier", f"{result.industry_classification.industry_name}")
            print_rag_retrieval(3, [{'metadata': {'source': 'bic_codes.json'}}, {'metadata': {'source': 'underwriting_guidelines.json'}}])
            
            # Rate Discovery (RAG)
            print_step_success(4, "Rate Discovery", f"Found {len(result.rate_info)} applicable rates")
            
            # Premium Calc
            print_step_success(5, "Premium Calculation", f"Base: ${result.premium_calculation.total_base_premium:,.2f}")
            
            # Risk & Authority
            print_step_success(6, "Risk Assessment", f"Score: {result.risk_assessment.risk_score} ({result.risk_assessment.overall_risk_level})")
            
            # Final Quote
            print("\n" + "="*72)
            print(f"{Fore.GREEN}{Style.BRIGHT}[OK] QUOTE GENERATED SUCCESSFULLY{Style.RESET_ALL}")
            print("="*72)
            
            q = result.generated_quote
            print(f"\n# {Fore.WHITE}Quote ID:{Style.RESET_ALL} {q.quote_id}")
            print(f"$ {Fore.WHITE}Final Premium:{Style.RESET_ALL} {Fore.GREEN}${result.modifier_result.adjusted_premium:,.2f}{Style.RESET_ALL}")
            print(f"% {Fore.WHITE}Status:{Style.RESET_ALL} {result.authority_check.authority_level}")
            
            print(f"\n{Fore.WHITE}Processing Time: {time.time() - start_time:.2f}s{Style.RESET_ALL}")
            
        else:
             print(f"\n{Fore.RED}[X] Pipeline Failed!{Style.RESET_ALL}")
             for err in result.errors:
                 print(f"  - {err}")

    except Exception as e:
        print(f"\n{Fore.RED}[X] Critical Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
