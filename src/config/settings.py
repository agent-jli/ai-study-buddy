"""
Configuration settings for the AI Study Buddy application.
Manages environment variables and application constants.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings and configuration."""

    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Model Configuration
    MODEL_NAME = "llama-3.1-8b-instant"
    TEMPERATURE = 0.9

    # Retry Configuration
    MAX_RETRIES = 3


# Global settings instance
settings = Settings()