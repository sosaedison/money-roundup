import datetime

from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

from moneyroundup.plaid_manager import client
from moneyroundup.supabase_client import supabase


def two_days_ago():
    today = datetime.datetime.now()
    return (today - datetime.timedelta(days=2)).date()


def yesterdays_date():
    today = datetime.datetime.now()
    return (today - datetime.timedelta(days=1)).date()


def fetch_transactions(access_token: str) -> int:
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=two_days_ago(),
        end_date=yesterdays_date(),
        options=TransactionsGetRequestOptions(),
    )
    response = client.transactions_get(request)
    return response["total_transactions"]


def populate_queue_with_transactions():
    # Get all active items from Supabase
    result = (
        supabase.table("items")
        .select("user_id, access_token")
        .eq("active", True)
        .execute()
    )

    for item in result.data:
        total_transactions = fetch_transactions(item["access_token"])
        # TODO: Send email with transaction summary
