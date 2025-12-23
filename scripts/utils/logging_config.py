import logging
import sys

def setup_logger(name: str, level=logging.INFO) -> logging.Logger:
    """
    Configures a standardized logger for the application.
    
    Why: 
    - Consistent formatting across all scripts.
    - Single point of change for log drivers (e.g., switching to JSON for Splunk).
    - Prevents duplicate handlers if called multiple times.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if setup_logger is called repeatedly
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)
        
    return logger
