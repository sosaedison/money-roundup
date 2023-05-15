from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

from moneyroundup.database import create_db_and_tables, drop_db_and_tables
from moneyroundup.plaid_manager import client as plaid
from moneyroundup.users import UserManager


@pytest_asyncio.fixture(scope="function", autouse=True)
async def rest_db():
    """Reset the database before each test."""
    await drop_db_and_tables()
    await create_db_and_tables()


@pytest.mark.asyncio
async def test_user_requests_link_token_with_valid_jwt(async_client: AsyncClient):
    # define a user
    new_user: dict[str, str] = {"email": "sosarocks@test.com", "password": "Sosa"}

    # register the user
    with patch.object(UserManager, "on_after_register", return_value=None):
        reg_res = await async_client.post("/api/auth/register", json=new_user)

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
        return_value={"link_token": "SIKE"},
    ):
        link_token_res = await async_client.post(
            "/api/link/token/create",
            headers={"Authorization": f"Bearer {access_token}"},  # <--- Valid JWT
        )

    assert link_token_res.status_code == 200
    assert link_token_res.json()["link_token"] is not None


@pytest.mark.asyncio
async def test_request_link_token_with_invalid_jwt(async_client: AsyncClient):
    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        link_token_res = await async_client.post(
            "/api/link/token/create",
            headers={"Authorization": f"Bearer SIKE"},  # <--- Invalid JWT
        )

    assert link_token_res.status_code == 401
    assert link_token_res.json()["detail"] == "Unauthorized"
