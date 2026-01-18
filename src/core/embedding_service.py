"""
Embedding service for generating and managing vector embeddings.
Uses Fireworks AI with Nomic embeddings.
"""

from functools import lru_cache
from typing import List, Dict, Any

from .fireworks_client import get_fireworks_client, FireworksClient


class EmbeddingService:
    """
    Service for generating embeddings for documents and queries.
    Uses Nomic AI embeddings via Fireworks for 768-dimensional vectors.
    """

    # Embedding dimensions for Nomic embed text v1.5
    EMBEDDING_DIMENSIONS = 768

    def __init__(self, client: FireworksClient):
        """Initialize with Fireworks client."""
        self.client = client

    def embed_document(self, text: str) -> List[float]:
        """
        Generate embedding for a document.
        Uses 'search_document' prefix for optimal retrieval performance.

        Args:
            text: Document text to embed

        Returns:
            768-dimensional embedding vector
        """
        return self.client.generate_embedding(
            text,
            prefix="search_document: "
        )

    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a search query.
        Uses 'search_query' prefix for optimal retrieval performance.

        Args:
            text: Query text to embed

        Returns:
            768-dimensional embedding vector
        """
        return self.client.generate_embedding(
            text,
            prefix="search_query: "
        )

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            texts: List of document texts

        Returns:
            List of embedding vectors
        """
        return self.client.generate_embeddings(
            texts,
            prefix="search_document: "
        )

    def prepare_document_for_storage(
        self,
        document: Dict[str, Any],
        text_field: str = "content"
    ) -> Dict[str, Any]:
        """
        Prepare a document for MongoDB storage with embedding.

        Args:
            document: Document dictionary
            text_field: Field containing text to embed

        Returns:
            Document with 'embedding' field added
        """
        if text_field not in document:
            raise ValueError(f"Document missing required field: {text_field}")

        text = document[text_field]
        embedding = self.embed_document(text)

        return {
            **document,
            "embedding": embedding
        }


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    """Get cached embedding service instance."""
    client = get_fireworks_client()
    return EmbeddingService(client)
