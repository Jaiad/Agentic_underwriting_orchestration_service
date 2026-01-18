"""
Configuration management using Pydantic Settings.
Loads environment variables from .env file with validation.
"""

from pathlib import Path
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Gemini Configuration
    google_api_key: Optional[str] = Field(
        default=None,
        description="Google API Key for Gemini"
    )

    # NVIDIA Configuration
    nvidia_api_key: Optional[str] = Field(
        default=None,
        description="NVIDIA NIM API Key"
    )
    nvidia_base_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        description="NVIDIA NIM Base URL"
    )
    # Defaulting to a strong model available on NIM
    nvidia_llm_model: str = Field(
        default="meta/llama-3.1-405b-instruct",
        description="NVIDIA LLM model"
    )

    # Fireworks AI Configuration
    fireworks_api_key: Optional[str] = Field(
        default=None,
        description="Fireworks AI API key"
    )
    fireworks_llm_model: str = Field(
        default="gemini-1.5-pro",
        description="LLM model for text generation"
    )
    fireworks_embedding_model: str = Field(
        default="models/text-embedding-004",
        description="Embedding model for vector search"
    )

    # MongoDB Configuration
    mongodb_uri: str = Field(
        default="mock",
        description="MongoDB connection URI"
    )
    mongodb_database: str = Field(
        default="insurance_underwriting",
        description="MongoDB database name"
    )

    # API Configuration
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)

    # Logging
    log_level: str = Field(default="INFO")

    # SSL Configuration (for corporate environments with proxy/firewall)
    ssl_verify: bool = Field(
        default=True,
        description="Set to False to disable SSL verification (corporate proxies)"
    )

    # Paths (computed)
    @property
    def project_root(self) -> Path:
        """Get project root directory."""
        return Path(__file__).parent.parent

    @property
    def data_dir(self) -> Path:
        """Get data directory path."""
        return self.project_root / "data"

    @property
    def quotes_dir(self) -> Path:
        """Get quotes output directory path."""
        quotes_path = self.project_root / "quotes"
        quotes_path.mkdir(exist_ok=True)
        return quotes_path

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are only loaded once.
    """
    return Settings()
