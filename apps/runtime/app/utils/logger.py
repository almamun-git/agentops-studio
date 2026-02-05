"""Application logger configuration."""

import logging
from app.core.config import settings

logger = logging.getLogger("agentops")


def configure_logger() -> logging.Logger:
    """Configure and return the application logger."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


configure_logger()

