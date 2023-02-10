import logging
import sys
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from pika.exceptions import AMQPConnectionError

from moneyroundup.fetch_transactions import populate_queue_with_transactions
from moneyroundup.rabbit_manager import RabbitManager
from moneyroundup.settings import settings

logging.basicConfig(
    filename=f"moneyroundup-{datetime.now().strftime('%m-%d-%Y')}.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def setup_app():
    if settings.ENV != "TEST":

        try:
            rabbit = RabbitManager(
                host=settings.RABBIT_HOST, queue=settings.RABBIT_QUEUE
            )
        except AMQPConnectionError:
            logging.critical("RABBITMQ FAILED TO CONNECT")
            sys.exit(0)

        # Create the non-blocking Background scheduler
        scheduler = BackgroundScheduler()
        # Run the fetch transactions job and run every 24 hours
        scheduler.add_job(
            populate_queue_with_transactions,
            "interval",
            seconds=int(settings.FETCH_TRANSACTIONS_INTERVAL),
            kwargs={"rabbit": rabbit},
        )
        scheduler.start()
