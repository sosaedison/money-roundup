from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from moneyroundup.plaid_manager import client as plaid
from tests.conftest import make_test_token


@pytest.mark.asyncio
async def test_create_link_token_for_authenticated_user(async_client: AsyncClient):
    token = make_test_token()

    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "McTesty"},
    ):
        res = await async_client.post(
            "/api/link/token/create",
            headers={"Authorization": f"Bearer {token}"},
        )

    assert res.json()["link_token"] == "McTesty"


def test_create_link_token_for_unauthenticated_user(client: TestClient):
    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        res = client.post("/api/link/token/create", json={"user_id": str(uuid4())})

    assert res.status_code == 401
