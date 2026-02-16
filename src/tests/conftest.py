import os
from uuid import uuid4

import jwt
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
    async with AsyncClient(app=app, base_url="http://localhost:8000") as ac:
        yield ac


def make_test_token(user_id: str | None = None, email: str = "test@example.com") -> str:
    """Create a valid Supabase-style JWT for testing."""
    payload = {
        "sub": user_id or str(uuid4()),
        "email": email,
        "aud": "authenticated",
        "role": "authenticated",
    }
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")
