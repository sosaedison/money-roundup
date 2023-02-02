from fastapi import Depends
from moneyroundup.plaid_manager import client
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from moneyroundup.models import User, Item
from moneyroundup.dependencies import get_db
from sqlalchemy.orm import Session
import datetime

from moneyroundup.rabbit_manager import QueueManager


def two_days_ago():
    today = datetime.datetime.now()
    two_days_ago = today - datetime.timedelta(days=2)
    return two_days_ago.date()


def yesterdays_date():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.date()


def fetch_transactions(access_token: str) -> int:

    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=two_days_ago(),
        end_date=yesterdays_date(),
        options=TransactionsGetRequestOptions(),
    )
    response = client.transactions_get(request)
    total_transactions = response["total_transactions"]

    return total_transactions


def populate_queue_with_transactions(
    rabbit: QueueManager, session: Session = Depends(get_db)
):

    with session.begin():
        users: list[User] = session.query(User).all()

        for user in users:

            items: list[Item] = (
                session.query(Item).filter(Item.user_id == user.id).all()
            )
            access_tokens: list[str] = [str(item.access_token) for item in items]

            total_transactions = 0
            for access_token in access_tokens:
                total_transactions += fetch_transactions(access_token=access_token)

            rabbit.produce(f"The total of your transactions was ${total_transactions}.")
