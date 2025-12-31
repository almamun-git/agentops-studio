import logging
from app.core.config import settings

logger = logging.getLogger("agentops")
logger.setLevel(logging.DEBUG if settings.env == "local" else logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

