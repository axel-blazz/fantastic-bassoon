from loguru import logger
import sys
from core.config import settings

def setup_logging():
    logger.remove() # Remove default logger


    is_dev = settings.ENV.lower() == "dev"

    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL.upper(),
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        enqueue=True,
        backtrace=is_dev,
        diagnose=is_dev
    )

    return logger

