from unittest.mock import patch
from uuid import uuid4

from fastapi.testclient import TestClient
from pytest import fixture

from moneyroundup.base import Base
from moneyroundup.database import engine
from moneyroundup.plaid_manager import client as plaid


@fixture(scope="function", autouse=True)
def rest_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_link_token_for_existing_user(client: TestClient):

    new_user = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    reg_res = client.post("/api/user", json=new_user)

    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        client_res = client.post(
            "/api/link/token/create",
            headers={"Authorization": f"Bearer {reg_res.json()['access_token']}"},
        )

        res: dict = client_res.json()

        assert res["link_token"] == "SIKE"


def test_create_link_token_for_non_existing_user(client: TestClient):

    new_user = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    res = client.post("/user", json=new_user)

    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        res = client.post("/api/link/token/create", json={"user_id": str(uuid4())})

    assert res.status_code == 401
