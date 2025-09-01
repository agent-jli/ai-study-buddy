"""
Prompt templates for the AI Study Buddy application.
Contains template functions for generating different types of questions.
"""


def get_mcq_prompt(topic: str, difficulty: str) -> str:
    """
    Generate multiple choice question prompt template.
    
    Args:
        topic: The topic for the question
        difficulty: The difficulty level ('easy', 'medium', 'hard')
        
    Returns:
        str: Formatted prompt for MCQ generation
    """
    return (
        f"Generate a {difficulty} multiple-choice question about {topic}.\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A clear, specific question\n"
        "- 'options': An array of exactly 4 possible answers\n"
        "- 'correct_answer': One of the options that is the correct answer\n\n"
        "Example format:\n"
        '{\n'
        '    "question": "What is the capital of France?",\n'
        '    "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '    "correct_answer": "Paris"\n'
        '}\n\n'
        "Your response:"
    )


def get_fill_blank_prompt(topic: str, difficulty: str) -> str:
    """
    Generate fill-in-the-blank question prompt template.
    
    Args:
        topic: The topic for the question
        difficulty: The difficulty level ('easy', 'medium', 'hard')
        
    Returns:
        str: Formatted prompt for fill-in-the-blank generation
    """
    return (
        f"Generate a {difficulty} fill-in-the-blank question about {topic}.\n\n"
        "Return ONLY a JSON object with these exact fields:\n"
        "- 'question': A sentence with '_____' marking where the blank should be\n"
        "- 'answer': The correct word or phrase that belongs in the blank\n\n"
        "Example format:\n"
        '{\n'
        '    "question": "The capital of France is _____.",\n'
        '    "answer": "Paris"\n'
        '}\n\n'
        "Your response:"
    )