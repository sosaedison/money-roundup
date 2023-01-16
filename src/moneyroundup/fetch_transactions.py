from moneyroundup.plaid_manager import client
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from moneyroundup.models import User, Item
from moneyroundup.dependencies import get_db
from sqlalchemy.orm import Session
import datetime


def two_days_ago():
    today = datetime.datetime.now()
    two_days_ago = today - datetime.timedelta(days=2)
    return two_days_ago.date()


def yesterdays_date():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.date()


def fetch_transactions():
    db_gen = get_db()
    session: Session = next(db_gen)

    # for each user, fetch all active access tokens
    with session.begin():
        users: list[User] = session.query(User).all()

    #   for each token, fetch transactions
    #       from the last 24 hours and sum
    with session.begin():
        for user in users:

            items: list[Item] = (
                session.query(Item).filter(Item.user_id == user.id).all()
            )
            access_tokens = [item.access_token for item in items]

            for access_token in access_tokens:
                request = TransactionsGetRequest(
                    access_token=access_token,
                    start_date=two_days_ago(),
                    end_date=yesterdays_date(),
                    options=TransactionsGetRequestOptions(),
                )
                response = client.transactions_get(request)
                transactions = response
                print(transactions)
