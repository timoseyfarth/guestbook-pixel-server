import os
import logging
from logging.handlers import RotatingFileHandler

# TODO fix double logger problem
def setup_logger(name: str = "guestbook_api") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    os.makedirs("logs", exist_ok=True)

    handler = RotatingFileHandler(
        "logs/guestbook_api.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger