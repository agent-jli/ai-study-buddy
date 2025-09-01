"""
Helper utilities for the AI Study Buddy application.
Contains the QuizManager class and utility functions for quiz management.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional

import streamlit as st
import pandas as pd

from src.generator.question_generator import QuestionGenerator


def rerun():
    """Toggle the rerun trigger to force Streamlit to rerun.
    Without rerun(), users would need to manually refresh the page 
    or interact with another widget to see the updated content. 
    This function provides immediate visual feedback by automatically 
    refreshing the app state and displaying new content 
    (like generated questions or quiz results) right after user actions.
    """
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)


class QuizManager:
    """Manages quiz generation, user interaction, and result evaluation."""

    def __init__(self):
        """Initialize the quiz manager with empty collections."""
        self.questions: List[Dict[str, Any]] = []
        self.user_answers: List[str] = []
        self.results: List[Dict[str, Any]] = []

    def generate_questions(
        self,
        generator: QuestionGenerator,
        topic: str,
        question_type: str,
        difficulty: str,
        num_questions: int
    ) -> bool:
        """
        Generate questions using the provided generator.
        
        Args:
            generator: The question generator instance
            topic: The topic for questions
            question_type: Type of questions ('Multiple Choice' or 'Fill in the Blank')
            difficulty: Difficulty level
            num_questions: Number of questions to generate
            
        Returns:
            bool: True if generation successful, False otherwise
        """
        # Reset collections
        self.questions = []
        self.user_answers = []
        self.results = []

        try:
            for _ in range(num_questions):
                if question_type == "Multiple Choice":
                    question = generator.generate_mcq(topic, difficulty.lower())
                    self.questions.append({
                        'type': 'MCQ',
                        'question': question.question,
                        'options': question.options,
                        'correct_answer': question.correct_answer
                    })
                else:
                    question = generator.generate_fill_blank(topic, difficulty.lower())
                    self.questions.append({
                        'type': 'Fill in the blank',
                        'question': question.question,
                        'correct_answer': question.answer
                    })

        except Exception as e:
            st.error(f"Error generating question: {e}")
            return False

        return True

    def attempt_quiz(self):
        """Display quiz questions and collect user answers."""
        for i, q in enumerate(self.questions):
            st.markdown(f"**Question {i + 1}: {q['question']}**")

            if q['type'] == 'MCQ':
                user_answer = st.radio(
                    f"Select an answer for Question {i + 1}",
                    q['options'],
                    key=f"mcq_{i}"
                )
            else:
                user_answer = st.text_input(
                    f"Fill in the blank for Question {i + 1}",
                    key=f"fill_blank_{i}"
                )

            # Ensure user_answers list is long enough
            while len(self.user_answers) <= i:
                self.user_answers.append("")
            
            self.user_answers[i] = user_answer

    def evaluate_quiz(self):
        """Evaluate the quiz and generate results."""
        self.results = []

        for i, (q, user_ans) in enumerate(zip(self.questions, self.user_answers)):
            result_dict = {
                'question_number': i + 1,
                'question': q['question'],
                'question_type': q["type"],
                'user_answer': user_ans,
                'correct_answer': q["correct_answer"],
                "is_correct": False
            }

            if q['type'] == 'MCQ':
                result_dict['options'] = q['options']
                result_dict["is_correct"] = user_ans == q["correct_answer"]
            else:
                result_dict['options'] = []
                result_dict["is_correct"] = (
                    user_ans.strip().lower() == q['correct_answer'].strip().lower()
                )

            self.results.append(result_dict)

    def generate_result_dataframe(self) -> pd.DataFrame:
        """
        Generate a pandas DataFrame from quiz results.
        
        Returns:
            pd.DataFrame: DataFrame containing quiz results
        """
        if not self.results:
            return pd.DataFrame()

        return pd.DataFrame(self.results)

    def save_to_csv(self, filename_prefix: str = "quiz_results") -> Optional[str]:
        """
        Save quiz results to a CSV file.
        
        Args:
            filename_prefix: Prefix for the filename
            
        Returns:
            str: Path to saved file, or None if saving failed
        """
        if not self.results:
            st.warning("No results to save!")
            return None

        df = self.generate_result_dataframe()

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{filename_prefix}_{timestamp}.csv"

        # Create results directory if it doesn't exist
        os.makedirs('results', exist_ok=True)
        full_path = os.path.join('results', unique_filename)

        try:
            df.to_csv(full_path, index=False)
            st.success("Results saved successfully!")
            return full_path

        except Exception as e:
            st.error(f"Failed to save results: {e}")
            return None
