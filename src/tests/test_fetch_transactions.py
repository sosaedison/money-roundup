from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import AsyncClient
from pytest import fixture

from moneyroundup.database import create_db_and_tables, drop_db_and_tables
from moneyroundup.fetch_transactions import populate_queue_with_transactions
from moneyroundup.plaid_manager import client
from moneyroundup.users import UserManager


@pytest_asyncio.fixture(scope="function", autouse=True)
async def rest_db():
    """Reset the database before each test."""
    await drop_db_and_tables()
    await create_db_and_tables()


@fixture()
def test_queue_manager():
    class TestQueueManager:
        # this class acts as a mock for the RabbitManager class
        def __init__(self) -> None:
            self.queue: list[str] = []

        def consume(self) -> str:
            ...

        def produce(self, message: str) -> bool:
            self.queue.append(message)
            return True

    return TestQueueManager()


@pytest.mark.asyncio
async def test_populate_queue_with_transactions(
    test_queue_manager, async_client: AsyncClient
):
    # define a user
    new_user: dict[str, str] = {"email": "sosarocks@test.com", "password": "Sosa"}

    # register the user
    with patch.object(UserManager, "on_after_register", return_value=None):
        client_res = await async_client.post("/api/auth/register", json=new_user)

    # assert that the user was created
    assert client_res.status_code == 201

    # get the user id
    user_id = client_res.json()["id"]

    # login with the new user
    client_res = await async_client.post(
        "/api/auth/jwt/login",
        data={"username": new_user["email"], "password": new_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert client_res.status_code == 200

    # get the access token
    access_token = client_res.json()["access_token"]

    # create item in database for this user
    item_res = await async_client.post(
        "/api/item",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json={"user_id": user_id, "access_token": "test_access_token"},
    )

    assert item_res.status_code == 201

    # create test QueueManager
    rabbit = test_queue_manager

    # create test transaction for plaid response
    plaid_client_response = {"total_transactions": 0}
    with patch.object(client, "transactions_get", return_value=plaid_client_response):
        await populate_queue_with_transactions(rabbit)

    assert len(rabbit.queue) == 1
