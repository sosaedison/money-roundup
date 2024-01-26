import datetime

from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from sqlalchemy import select

from moneyroundup.database import get_async_session_context_manager
from moneyroundup.dependencies import get_db
from moneyroundup.models import Item, User
from moneyroundup.plaid_manager import client

db = get_db()


def two_days_ago():
    today = datetime.datetime.now()
    two_days_ago = today - datetime.timedelta(days=2)
    return two_days_ago.date()


def yesterdays_date():
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.date()


def fetch_total_transactions(access_token: str) -> int:
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=two_days_ago(),
        end_date=yesterdays_date(),
        options=TransactionsGetRequestOptions(),
    )
    response = client.transactions_get(request)
    total_transactions = response["total_transactions"]

    return total_transactions


async def populate_queue_with_transactions(session=get_async_session_context_manager):
    async with session() as session:
        result = await session.execute(select(User))
        users = [{"id": u.id, "email": u.email} for u in result.scalars()]

        for user in users:
            items = await session.execute(
                select(Item).where(Item.user_id == str(user.get("id")))
            )
            items = [
                {"user_id": item.user_id, "access_token": item.access_token}
                for item in items.scalars()
            ]

            access_tokens: list[str] = [str(item.get("access_token")) for item in items]

            total_transactions = 0
            for access_token in access_tokens:
                total_transactions += fetch_total_transactions(
                    access_token=access_token
                )
