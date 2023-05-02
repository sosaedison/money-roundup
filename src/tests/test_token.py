from unittest.mock import patch
import pytest
import pytest_asyncio
from httpx import AsyncClient

from uuid import uuid4

from fastapi.testclient import TestClient

from moneyroundup.plaid_manager import client as plaid
from moneyroundup.database import create_db_and_tables, drop_db_and_tables


@pytest_asyncio.fixture(scope="function", autouse=True)
async def rest_db():
    """Reset the database before each test."""
    await drop_db_and_tables()
    await create_db_and_tables()


@pytest.mark.asyncio
async def test_create_link_token_for_existing_user(async_client: AsyncClient):

    # define a user
    new_user: dict[str, str] = {"email": "sosarocks@test.com", "password": "Sosa"}

    # register the user
    reg_res = await async_client.post("/api/auth/register", json=new_user)

    # assert that the user was created
    assert reg_res.status_code == 201

    # login with the new user
    client_res = await async_client.post(
        "/api/auth/jwt/login",
        data={"username": new_user["email"], "password": new_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert client_res.status_code == 200

    # get the access token
    access_token = client_res.json()["access_token"]

    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "McTesty"},
    ):
        client_res = await async_client.post(
            "/api/link/token/create",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        res: dict = client_res.json()

        assert res["link_token"] == "McTesty"


def test_create_link_token_for_non_existing_user(client: TestClient):

    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        res = client.post("/api/link/token/create", json={"user_id": str(uuid4())})

    assert res.status_code == 401
