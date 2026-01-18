
"""
LangChain RAG Tutorial (Advanced)
---------------------------------
This file demonstrates how to build a specialized Retrieval-Augmented Generation (RAG)
pipeline using the working Gemini 2.0 Flash model.

CONCEPTS DEMONSTRATED:
1.  **Document Loading & Splitting**: Preparing knowledge bases.
2.  **Vector Embeddings**: Converting text to numbers using Google's models.
3.  **FAISS Vector Store**: Efficient similarity result.
4.  **Retrieval Chain**: The "R" in RAG - finding relevant context.
5.  **Contextual Answer Generation**: The "G" in RAG.

Usage:
    python langchain_rag_tutorial.py
"""

import os
import sys
import warnings
import urllib3
import requests

# --- SSL PATCH (Crucial for execution) ---
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''
os.environ['PYTHONHTTPSVERIFY'] = '0'

old_merge = requests.Session.merge_environment_settings
def new_merge(self, url, proxies, stream, verify, cert):
    return old_merge(self, url, proxies, stream, False, cert)
requests.Session.merge_environment_settings = new_merge
# -----------------------------------------

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Load Environment
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

def main():
    print("🚀 Starting LangChain RAG Tutorial...")
    
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found.")
        return

    # ==========================
    # 1. Create Dummy Knowledge
    # ==========================
    # In a real app, you would load this from PDFs or Text files.
    knowledge_base_text = """
    INSURANCE UNDERWRITING GUIDELINES (2025 EDITION)
    
    1. CONSTRUCTION RISKS:
       - Base Rate: $8.50 per $1,000 of revenue.
       - Height Exposure: Any work above 4 stories requires a 'High Altitude' endorsement.
       - Tools Coverage: Limited to $5,000 per item unless scheduled.
    
    2. TECHNOLOGY / SAAS:
       - Base Rate: $0.50 per $1,000 of revenue (Low Risk).
       - Cyber Liability: MANDATORY for all SaaS companies storing PII.
       - Remote Work: 100% remote workforce qualifies for a 15% 'Digital Nomad' discount.
    
    3. RESTAURANTS:
       - Alcohol Sales: If alcohol is > 40% of revenue, liquor liability premium triples.
       - Deep Fryers: Automatic extinguishing systems (Ansul) are required.
    """
    
    # Save to a temp file to demonstrate TextLoader
    with open("temp_guidelines.txt", "w") as f:
        f.write(knowledge_base_text)

    # ==========================
    # 2. Load & Split
    # ==========================
    print("\n--- 📚 Indexing Knowledge Base ---")
    loader = TextLoader("temp_guidelines.txt")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    splits = splitter.split_documents(docs)
    print(f"Created {len(splits)} distinct knowledge chunks.")

    # ==========================
    # 3. Embed & Store
    # ==========================
    print("\n--- 🧠 Creating Embeddings ---")
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=api_key
    )
    
    # Using FAISS (Facebook AI Similarity Search)
    vectorstore = FAISS.from_documents(splits, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # ==========================
    # 4. Define the Chain (LCEL)
    # ==========================
    print("\n--- 🔗 Building RAG Chain ---")
    
    # We use the WORKING model identified earlier
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0
    )

    template = """You are a helpful underwriting assistant. 
    Answer the question based ONLY on the following context:
    {context}
    
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # ==========================
    # 5. Execute Queries
    # ==========================
    print("\n" + "="*50)
    print("🤖 RAG ASSISTANT READY")
    print("="*50)

    questions = [
        "What is the base rate for a Tech company?",
        "Do I need an endorsement for work above 4 stories?",
        "What is the rule for deep fryers?"
    ]

    for q in questions:
        print(f"\n❓ Question: {q}")
        print("   Thinking...", end="\r")
        answer = rag_chain.invoke(q)
        print(f"💡 Answer:   {answer.strip()}")
        print("-" * 30)

    # Cleanup
    if os.path.exists("temp_guidelines.txt"):
        os.remove("temp_guidelines.txt")

if __name__ == "__main__":
    main()
