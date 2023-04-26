import os

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from pytest import fixture

os.environ["ENV"] = "TEST"

from moneyroundup.main import app
from moneyroundup.settings import settings


@fixture
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

    return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)[
        "sub"
    ]
