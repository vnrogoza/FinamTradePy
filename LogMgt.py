import logging

# LogMgt.py
"""
Module: LogMgt
Description: This module provides logging management functionality for the application.
"""


def initialize_logger(name: str, log_file: str, level: int = logging.INFO) -> logging.Logger:
    """
    Initializes and returns a logger instance.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (default: logging.INFO).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    return logger

# Example usage
if __name__ == "__main__":
    log = initialize_logger("LogMgt", "app.log")
    log.info("Logger initialized successfully.")