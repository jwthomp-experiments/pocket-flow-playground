"""Logging configuration for the Pocket Flow Playground project."""

import logging
import sys


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure and return a logger instance.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logging.Logger instance
    """
    # Create logger
    logger = logging.getLogger("pocket_flow_playground")
    logger.setLevel(log_level.upper())

    # Prevent adding multiple handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level.upper())

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    return logger


# Default logger instance
logger = setup_logging()
