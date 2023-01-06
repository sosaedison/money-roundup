from uuid import uuid4
from unittest.mock import patch
from pytest import fixture
from fastapi.testclient import TestClient

from app.src.schemas import NewUser, LoggedInUser, LinkTokenForUser
from app.src.base import Base
from app.src.database import engine
from app.src.plaid_manager import client as plaid


@fixture(scope="function", autouse=True)
def rest_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# @patch("client.link_token_create")
def test_create_link_token_for_existing_user(client: TestClient):
    # link_token_create.return_value = {"link_token": "SIKE"}

    new_user: NewUser = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    res = client.post("/user", json=new_user)

    user: LoggedInUser = res.json()

    new_user_id = user["user_id"]
    with patch.object(
        plaid,
        "link_token_create",
        return_value={"link_token": "SIKE"},
    ):
        res = client.post("/link/token/create", json={"user_id": user["user_id"]})

        res: LinkTokenForUser = res.json()
        print(res)

    assert res["user_id"] == new_user_id
    assert res["link_token"] == "SIKE"


# def test_create_link_token_for_non_existing_user(client: TestClient):

#     new_user: NewUser = {
#         "email": "sosarocks@test.com",
#         "first_name": "Sosa",
#         "last_name": "Rocks",
#         "profile_pic_url": "http://www.some_cool_pic.com",
#     }

#     res = client.post("/user", json=new_user)

#     res = client.post("/link/token/create", json={"user_id": str(uuid4())})

#     assert res.status_code == 401
