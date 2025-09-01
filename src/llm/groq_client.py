"""
Groq LLM client module for the AI Study Buddy application.
Handles communication with the Groq API for question generation.
"""

from groq import Groq
from src.config.settings import settings


def get_groq_client() -> Groq:
    """
    Create and return a Groq client instance.
    
    Returns:
        Groq: Configured Groq client
    """
    return Groq(api_key=settings.GROQ_API_KEY)


def generate_completion(client: Groq, prompt: str) -> str:
    """
    Generate completion using Groq client.
    
    Args:
        client: The Groq client instance
        prompt: The prompt to send to the model
        
    Returns:
        str: The generated response content
    """
    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=settings.TEMPERATURE
    )
    return response.choices[0].message.content