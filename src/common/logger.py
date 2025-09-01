"""
Logging configuration for the AI Study Buddy application.
Sets up centralized logging with daily log rotation.
"""

import logging
import os
from datetime import datetime

# Constants
LOGS_DIR = "logs"

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate log filename with current date
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure basic logging
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO,
    filemode='a'
)


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name: Name for the logger (typically __name__ or class name)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger