from fastapi.testclient import TestClient

from tests.conftest import decode_token


def test_user_registration(client: TestClient):

    new_user: dict[str, str] = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    client_res = client.post("/api/user", json=new_user)

    res: dict = client_res.json()

    assert set(
        [
            "access_token",
            "first_name",
            "last_name",
            "profile_pic_url",
            "email",
        ]
    ).issubset(
        list(res.keys())
    )  # successful registration


def test_user_login(
    client: TestClient,
):

    new_user: dict[str, str] = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    client_res = client.post("/api/user", json=new_user)

    new_user_id = decode_token(client_res.json()["access_token"])

    client_res = client.post("/api/user", json=client_res.json())

    assert (
        decode_token(client_res.json()["access_token"]) == new_user_id
    )  # successful login
