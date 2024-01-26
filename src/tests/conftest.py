import os
from typing import Any, AsyncGenerator
from unittest.mock import patch

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from moneyroundup.users import UserManager

os.environ["ENV"] = "TEST"

from moneyroundup.dependencies import get_secret_value  # noqa: E402
from moneyroundup.main import app  # noqa: E402
from moneyroundup.settings import get_settings  # noqa: E402

settings = get_settings()


@pytest.fixture
def client():
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture
async def async_client():
    """Create a test client for the app."""
    from moneyroundup.main import app

    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


def decode_token(token: str) -> str:
    """Decode a JWT token and return the user id."""
    from jose import jwt

    return jwt.decode(
        token,
        key=get_secret_value(settings.APP_SECRET_KEY),
        algorithms=settings.JWT_ALGORITHM,
    )["sub"]


@pytest.fixture
def new_user() -> dict[str, str | bool]:
    return {"email": "sosarocks@test.com", "password": "Sosa"}


@pytest_asyncio.fixture
async def create_new_user_and_token(
    async_client: AsyncClient, new_user: dict[str, str]
) -> AsyncGenerator[tuple[dict, str], Any]:
    """Create a new user."""
    with patch.object(UserManager, "on_after_register", return_value=None):
        reg_res = await async_client.post("/api/auth/register", json=new_user)

    assert reg_res.status_code == 201

    client_res = await async_client.post(
        "/api/auth/jwt/login",
        data={"username": new_user["email"], "password": new_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert client_res.status_code == 200

    # get the access token
    access_token = client_res.json()["access_token"]

    # get the user from the database
    client_res = await async_client.get(
        "/api/auth/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    yield (client_res.json(), access_token)
