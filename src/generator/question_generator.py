"""
Question generator module for the AI Study Buddy application.
Handles the generation of different types of questions using Groq LLM.
"""

import json
from typing import Union

from src.models.question_schemas import MCQQuestion, FillBlankQuestion
from src.prompts.templates import get_mcq_prompt, get_fill_blank_prompt
from src.llm.groq_client import get_groq_client, generate_completion
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException


class QuestionGenerator:
    """Generates different types of questions using AI."""

    def __init__(self):
        """Initialize the question generator with Groq client and logger."""
        self.client = get_groq_client()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(
        self,
        prompt: str,
        model_class: Union[MCQQuestion, FillBlankQuestion],
        topic: str,
        difficulty: str
    ):
        """
        Retry generation and parse JSON response.
        
        Args:
            prompt: The prompt to send to the LLM
            model_class: The Pydantic model class to validate against
            topic: The topic for the question
            difficulty: The difficulty level
            
        Returns:
            Parsed question instance
            
        Raises:
            CustomException: If generation fails after max retries
        """
        for attempt in range(settings.MAX_RETRIES):
            try:
                self.logger.info(
                    f"Generating question for topic '{topic}' "
                    f"with difficulty '{difficulty}' (attempt {attempt + 1})"
                )

                response = generate_completion(self.client, prompt)

                # Clean the response to extract JSON
                response_clean = response.strip()
                if response_clean.startswith('```json'):
                    response_clean = response_clean[7:]
                if response_clean.endswith('```'):
                    response_clean = response_clean[:-3]
                response_clean = response_clean.strip()

                # Parse JSON and create model instance
                json_data = json.loads(response_clean)
                parsed = model_class(**json_data)

                self.logger.info("Successfully parsed the question")
                return parsed

            except Exception as e:
                self.logger.error(f"Error occurred: {str(e)}")
                if attempt == settings.MAX_RETRIES - 1:
                    raise CustomException(
                        f"Generation failed after {settings.MAX_RETRIES} attempts", e
                    )

    def generate_mcq(self, topic: str, difficulty: str = 'medium') -> MCQQuestion:
        """
        Generate a multiple choice question.
        
        Args:
            topic: The topic for the question
            difficulty: The difficulty level ('easy', 'medium', 'hard')
            
        Returns:
            MCQQuestion instance
            
        Raises:
            CustomException: If MCQ generation fails
        """
        try:
            prompt = get_mcq_prompt(topic, difficulty)
            question = self._retry_and_parse(prompt, MCQQuestion, topic, difficulty)

            # Validate MCQ structure
            if len(question.options) != 4:
                raise ValueError("MCQ must have exactly 4 options")
            if question.correct_answer not in question.options:
                raise ValueError("Correct answer must be one of the options")

            self.logger.info("Generated a valid MCQ Question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate MCQ: {str(e)}")
            raise CustomException("MCQ generation failed", e)

    def generate_fill_blank(self, topic: str, difficulty: str = 'medium') -> FillBlankQuestion:
        """
        Generate a fill-in-the-blank question.
        
        Args:
            topic: The topic for the question
            difficulty: The difficulty level ('easy', 'medium', 'hard')
            
        Returns:
            FillBlankQuestion instance
            
        Raises:
            CustomException: If fill-in-the-blank generation fails
        """
        try:
            prompt = get_fill_blank_prompt(topic, difficulty)
            question = self._retry_and_parse(prompt, FillBlankQuestion, topic, difficulty)

            # Validate fill-in-the-blank structure
            if "___" not in question.question:
                raise ValueError("Fill-in-the-blank question must contain '___'")

            self.logger.info("Generated a valid Fill-in-the-Blank Question")
            return question

        except Exception as e:
            self.logger.error(f"Failed to generate fill-in-the-blank: {str(e)}")
            raise CustomException("Fill-in-the-blank generation failed", e)

