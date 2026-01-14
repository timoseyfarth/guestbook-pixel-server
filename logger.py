import os
import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = "guestbook_api") -> logging.Logger:
    """
    Sets up a logger with a RotatingFileHandler and a StreamHandler.
    Ensures that handlers are only added once to prevent duplicate logs.
    """
    logger = logging.getLogger(name)
    
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        os.makedirs("logs", exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = RotatingFileHandler(
            "logs/guestbook_api.log",
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()