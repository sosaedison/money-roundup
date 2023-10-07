import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from moneyroundup.fetch_transactions import populate_queue_with_transactions
from moneyroundup.settings import get_settings

settings = get_settings()

logging.basicConfig(
    filename=f"moneyroundup-{datetime.now().strftime('%m-%d-%Y')}.log",
    level=settings.LOGGING_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def setup_app():
    if settings.ENV != "TEST":
        # Create the non-blocking Background scheduler
        scheduler = AsyncIOScheduler()
        # add the fetch transactions job and run every 24 hours
        scheduler.add_job(
            populate_queue_with_transactions,
            "interval",
            seconds=settings.FETCH_TRANSACTIONS_INTERVAL,
        )
        scheduler.start()
