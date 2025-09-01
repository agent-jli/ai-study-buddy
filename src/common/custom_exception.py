"""
Custom exception classes for the AI Study Buddy application.
Provides enhanced error tracking with file and line information.
"""

import sys
from typing import Optional


class CustomException(Exception):
    """Custom exception with enhanced error details."""

    def __init__(self, message: str, error_detail: Optional[Exception] = None):
        """
        Initialize custom exception with detailed error information.
        
        Args:
            message: Human-readable error message
            error_detail: Original exception that caused this error (optional)
        """
        self.error_message = self.get_detailed_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_detailed_error_message(message: str, error_detail: Optional[Exception]) -> str:
        """
        Generate detailed error message with file and line information.
        
        Args:
            message: Base error message
            error_detail: Original exception details
            
        Returns:
            str: Formatted error message with context
        """
        _, _, exc_tb = sys.exc_info()
        
        if exc_tb:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "Unknown File"
            line_number = "Unknown Line"
            
        error_info = f"Error: {error_detail}" if error_detail else "No additional error details"
        
        return f"{message} | {error_info} | File: {file_name} | Line: {line_number}"

    def __str__(self) -> str:
        """Return the detailed error message."""
        return self.error_message