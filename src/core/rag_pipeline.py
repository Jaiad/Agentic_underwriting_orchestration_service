"""
RAG Pipeline Implementation using LangChain LCEL.
Follows the user's requested architecture: Load -> Split -> Embed -> FAISS -> Chain.
"""

import os
import logging
from typing import Optional

# LangChain Imports
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Google Integration
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# Try importing VertexAI, but don't fail if dependencies are missing/misconfigured
try:
    from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI
    VERTEX_AVAILABLE = True
except ImportError:
    VERTEX_AVAILABLE = False

# Local Imports
from src.config import get_settings
from src.core.data_loader import load_documents
from src.core.ssl_handler import configure_ssl_handling

# Ensure SSL patches are applied
configure_ssl_handling()
logger = logging.getLogger(__name__)

class RAGPipeline:
    """
    Encapsulates the RAG logic using LangChain LCEL.
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.vectorstore = None
        self.retriever = None
        self.rag_chain = None
        self.llm = None
        self._initialized = False
        
        # Setup Google API Key if provided
        if self.settings.google_api_key:
            os.environ["GOOGLE_API_KEY"] = self.settings.google_api_key
            
        # DO NOT initialize pipeline here - do it lazily on first query
        logger.info("RAGPipeline ready (will initialize on first query)")

    def _initialize_pipeline(self):
        """Initialize the entire RAG pipeline with optimizations for web UI."""
        logger.info("🚀 Initializing RAG Pipeline (Optimized for Web)...")

        try:
            # 1. Load Documents
            docs = load_documents(str(self.settings.data_dir))
            if not docs:
                logger.warning("No documents found in data directory!")
                return

            # 2. Split - REDUCED for faster processing
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,  # Reduced from 1000
                chunk_overlap=50  # Reduced from 150
            )
            chunks = splitter.split_documents(docs)
            
            # LIMIT chunks for faster embedding
            if len(chunks) > 50:
                chunks = chunks[:50]
                logger.info(f"Limited to 50 chunks for fast web response")
            
            logger.info(f"Loaded {len(docs)} documents; using {len(chunks)} chunks.")

            # 3. Embed & Vector Store (FAISS)
            use_vertex = VERTEX_AVAILABLE and os.getenv("GOOGLE_CLOUD_PROJECT")
            
            if use_vertex:
                logger.info("Using VertexAI Embeddings")
                embeddings = VertexAIEmbeddings(model_name="text-embedding-004")
            else:
                logger.info("Using Google Generative AI Embeddings (API Key)")
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/text-embedding-004",
                    request_timeout=10  # Add timeout
                )

            # Create Vector Store
            self.vectorstore = FAISS.from_documents(chunks, embeddings)
            self.retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": 2}  # Reduced from 4 for speed
            )

            # 4. LLM Setup with timeouts
            if use_vertex:
                logger.info("Using VertexAI LLM")
                self.llm = ChatVertexAI(
                    model="gemini-1.5-flash",
                    temperature=0,
                    request_timeout=15
                ) 
            else:
                logger.info("Using Google Generative AI LLM (API Key)")
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash-exp",
                    temperature=0,
                    convert_system_message_to_human=True,
                    request_timeout=15  # 15 second timeout
                )

            # 5. LCEL Chain Construction - SIMPLIFIED
            template = """Use context to answer briefly. If unknown, say 'I don't know'.
            
            Context: {context}
            
            Question: {question}
            """
            
            prompt = ChatPromptTemplate.from_template(template)
            
            def format_docs(docs):
                return "\n\n".join([d.page_content for d in docs])

            # The Chain
            self.rag_chain = (
                RunnableParallel({
                    "context": self.retriever | format_docs,
                    "question": RunnablePassthrough()
                })
                | prompt
                | self.llm
                | StrOutputParser()
            )
            logger.info("✅ RAG Chain Ready (Optimized)")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG pipeline: {e}")
            logger.warning("RAG will not be available for this session")
            self.vectorstore = None
            self.retriever = None
            self.rag_chain = None

    def query(self, question: str) -> str:
        """Run the RAG chain."""
        # Lazy initialization on first query
        if not self._initialized:
            logger.info("First query received - initializing RAG pipeline now...")
            self._initialize_pipeline()
            self._initialized = True
            
        if not self.rag_chain:
            return "RAG Pipeline not initialized (embeddings may have failed)."
        return self.rag_chain.invoke(question)

# Singleton instance
_pipeline_instance = None

def get_rag_pipeline() -> RAGPipeline:
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = RAGPipeline()
    return _pipeline_instance
