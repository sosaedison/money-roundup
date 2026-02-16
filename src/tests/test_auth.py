import pytest
from httpx import AsyncClient

from tests.conftest import make_test_token


@pytest.mark.asyncio
async def test_me_with_valid_token(async_client: AsyncClient):
    token = make_test_token(email="sosarocks@test.com")

    res = await async_client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    assert res.json()["email"] == "sosarocks@test.com"


@pytest.mark.asyncio
async def test_me_with_no_token(async_client: AsyncClient):
    res = await async_client.get("/api/auth/me")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token(async_client: AsyncClient):
    res = await async_client.get(
        "/api/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert res.status_code == 401
