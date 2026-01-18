"""
Step 2: Industry Classifier
Determines the Business Industry Classification (BIC) code for the client.
"""

from src.core.fireworks_client import FireworksClient
from src.core.vector_search import VectorSearchService
from src.core.mongodb_client import Collections
from src.prompts import INDUSTRY_CLASSIFIER_SYSTEM, INDUSTRY_CLASSIFIER_PROMPT
from src.pipeline.models import ExtractedEmail, IndustryClassification


class IndustryClassifierStep:
    """
    Classifies the business into an industry category using BIC codes.
    Uses vector search to find relevant classifications and LLM to select best match.
    """

    def __init__(self, llm_client: FireworksClient, vector_search: VectorSearchService, rag_pipeline=None):
        """Initialize with LLM client, vector search, and optional RAG pipeline."""
        self.llm_client = llm_client
        self.vector_search = vector_search
        self.rag_pipeline = rag_pipeline

    def execute(self, extracted_email: ExtractedEmail) -> IndustryClassification:
        """
        Classify industry based on email and optional RAG context.
        Args:
            extracted_email: Parsed email data

        Returns:
            IndustryClassification with BIC code and details
        """
        # Get RAG context if available
        rag_context = ""
        if self.rag_pipeline:
            # Query for industry specific info
            query = f"Industry classification for {extracted_email.industry_description}"
            rag_context = self.rag_pipeline.query(query)
            
        # Use RAG context in prompt (conceptually - simplistic integration for now)
        # In a full implementation, we'd append this to the system prompt
        
        # Build search query from business description
        search_query = f"{extracted_email.industry_description} {extracted_email.client_name}"

        # Search for matching BIC codes
        # UPDATED: Use local FAISS RAG via rag_pipeline instead of MongoDB (which is failing DNS)
        rag_context_str = ""
        if self.rag_pipeline:
            # We already queried above, let's use that result
            rag_context_str = rag_context
        else:
            # Fallback if no RAG
            rag_context_str = "No specific classification guidelines available."

        # Format context for LLM
        prompt = INDUSTRY_CLASSIFIER_PROMPT.format(
            business_description=extracted_email.industry_description,
            bic_codes_context=rag_context_str,
        )

        result = self.llm_client.generate_json(
            prompt=prompt,
            system_prompt=INDUSTRY_CLASSIFIER_SYSTEM,
            temperature=0.1,
        )

        return IndustryClassification(
            bic_code=result.get("bic_code", "99"),
            industry_name=result.get("industry_name", "Unknown"),
            risk_category=result.get("risk_category", "MEDIUM"),
            confidence_score=float(result.get("confidence_score", 0.5)),
            matching_keywords=result.get("matching_keywords", []),
            subcategory=result.get("subcategory"),
        )
