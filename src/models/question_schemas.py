"""
Question schema models for the AI Study Buddy application.
Defines data structures for different question types using Pydantic.
"""

from typing import List
from pydantic import BaseModel, Field, validator


class MCQQuestion(BaseModel):
    """Multiple Choice Question Schema."""

    question: str = Field(description="The question text")
    options: List[str] = Field(description="List of 4 options")
    correct_answer: str = Field(description="The correct answer from the options")

    # validator for question field
    @validator('question', pre=True)
    def clean_question(cls, v):
        """Clean and validate question text."""
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)


class FillBlankQuestion(BaseModel):
    """Fill in the Blank Question Schema."""

    question: str = Field(description="The question text with '___' for the blank")
    answer: str = Field(description="The correct word or phrase for the blank")

    # validator for question field
    @validator('question', pre=True)
    def clean_question(cls, v):
        """Clean and validate question text."""
        if isinstance(v, dict):
            return v.get('description', str(v))
        return str(v)
