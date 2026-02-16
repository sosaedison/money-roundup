from unittest.mock import patch

import pytest
from httpx import AsyncClient

from moneyroundup.plaid_manager import client as plaid
from tests.conftest import make_test_token


@pytest.mark.asyncio
async def test_user_requests_link_token_with_valid_jwt(async_client: AsyncClient):
    token = make_test_token()

    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        res = await async_client.post(
            "/api/link/token/create",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert res.status_code == 200
    assert res.json()["link_token"] is not None


@pytest.mark.asyncio
async def test_request_link_token_with_invalid_jwt(async_client: AsyncClient):
    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        res = await async_client.post(
            "/api/link/token/create",
            headers={"Authorization": "Bearer SIKE"},
        )

    assert res.status_code == 401
