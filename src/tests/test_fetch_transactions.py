from unittest.mock import patch

import pytest

from moneyroundup.fetch_transactions import populate_queue_with_transactions
from moneyroundup.plaid_manager import client
from moneyroundup.supabase_client import supabase


@pytest.mark.asyncio
async def test_populate_queue_with_transactions():
    mock_items = {"data": [{"user_id": "test-uid", "access_token": "test_access_token"}]}

    plaid_response = {"total_transactions": 0}

    with patch.object(
        supabase.table("items"), "execute", return_value=type("R", (), {"data": mock_items["data"]})()
    ):
        with patch.object(client, "transactions_get", return_value=plaid_response):
            # This test just verifies no exceptions are raised
            populate_queue_with_transactions()
