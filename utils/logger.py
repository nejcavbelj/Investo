"""
Unified logging setup for Investo
"""

import logging
import sys
from pathlib import Path
from config.settings import PROJECT_ROOT, LOG_LEVEL, LOG_FORMAT

def setup_logger(name="investo", level=LOG_LEVEL):
    """Set up a logger with consistent formatting"""
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(log_dir / "investo.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name="investo"):
    """Get a logger instance"""
    return logging.getLogger(name)

# Set up default logger
default_logger = setup_logger()
