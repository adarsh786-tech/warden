"""
Configuration module for the Compliance Audit Agent.
Manages API keys, model settings, and system parameters.
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the compliance audit system."""
    
    # Grok API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROK_API_BASE: str = "https://api.x.ai/v1"
    GROK_MODEL: str = "grok-beta"  # or "grok-2-latest" depending on your access
    
    # Model Parameters
    TEMPERATURE: float = 0.1  # Low temperature for consistent, deterministic outputs
    MAX_TOKENS: int = 4000
    
    # Compliance Thresholds
    COMPLIANCE_PASS_THRESHOLD: float = 85.0  # Minimum % to pass audit
    HIGH_SEVERITY_THRESHOLD: int = 3  # Max critical issues before failing
    
    # Reflection Loop Settings
    ENABLE_REFLECTION: bool = True
    MAX_REFLECTION_ITERATIONS: int = 2
    CONFIDENCE_THRESHOLD: float = 0.8  # Trigger reflection if confidence < this
    
    # File Paths
    MOCK_DOCS_PATH: str = "data/mock_docs"
    MOCK_RULES_PATH: str = "data/mock_rules"
    MOCK_REPO_PATH: str = "data/mock_repo"
    OUTPUT_PATH: str = "output"
    
    # API Settings (for FastAPI)
    UPLOAD_FOLDER: str = "uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: set = {'.txt', '.md', '.py', '.json', '.yaml', '.yml', '.xml', '.js', '.java', '.go'}
    CORS_ORIGINS: list = ["*"]  # Allow all origins for now, restrict in production
    
    # Logging
    LOG_LEVEL: str = "INFO"
    VERBOSE: bool = True
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in your .env file."
            )
        return True
    
    @classmethod
    def get_llm_config(cls) -> dict:
        """Return LLM configuration dictionary."""
        return {
            "api_key": cls.GROQ_API_KEY,
            "base_url": cls.GROK_API_BASE,
            "model": cls.GROK_MODEL,
            "temperature": cls.TEMPERATURE,
            "max_tokens": cls.MAX_TOKENS,
        }


# Validate configuration on import
Config.validate()