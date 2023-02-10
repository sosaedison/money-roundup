from fastapi.testclient import TestClient
from jose import jwt

from moneyroundup.settings import settings


def test_user_requests_link_token_with_valid_jwt(client: TestClient):
    new_user: dict[str, str] = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    reg_res = client.post("/api/user", json=new_user)

    assert reg_res.status_code == 200

    token = jwt.decode(
        reg_res.json()["access_token"],
        settings.SECRET_KEY,
        algorithms=settings.JWT_ALGORITHM,
    )

    link_token_res = client.post(
        "/api/link/token/create",
        json={
            "user_id": token["sub"],
            "access_token": reg_res.json()["access_token"],
        },
    )

    assert link_token_res.status_code == 200
    assert link_token_res.json()["link_token"] is not None


def test_request_link_token_with_invalid_jwt(client: TestClient):
    new_user: dict[str, str] = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    reg_res = client.post("/api/user", json=new_user)

    assert reg_res.status_code == 200

    token = jwt.decode(
        reg_res.json()["access_token"],
        settings.SECRET_KEY,
        algorithms=settings.JWT_ALGORITHM,
    )

    link_token_res = client.post(
        "/api/link/token/create",
        json={
            "user_id": token["sub"],
            "access_token": "invalid_token",
        },
    )

    assert link_token_res.status_code == 401
    assert link_token_res.json()["detail"] == "Could not validate credentials"
