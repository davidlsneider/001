"""
Logging configuration for the trading bot
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = 'swarm_trading_bot',
    log_file: Optional[str] = None,
    log_level: str = 'INFO'
) -> logging.Logger:
    """
    Set up and configure logger

    Args:
        name: Logger name
        log_file: Path to log file (optional)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler (if log file specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = 'swarm_trading_bot') -> logging.Logger:
    """Get existing logger instance"""
    return logging.getLogger(name)
