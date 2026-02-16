import logging
from datetime import datetime

from moneyroundup.settings import settings

logging.basicConfig(
    filename=f"moneyroundup-{datetime.now().strftime('%m-%d-%Y')}.log",
    level=settings.LOGGING_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
