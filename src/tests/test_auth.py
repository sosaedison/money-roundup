import time

from fastapi.testclient import TestClient
from pytest import fixture

from moneyroundup.base import Base
from moneyroundup.database import engine


@fixture(scope="function", autouse=True)
def rest_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_user_register_and_gets_jwt(client: TestClient):
    """Test that a user can register and get a JWT token."""
    # Register a user
    new_user: dict[str, str] = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    # register new user
    client_res = client.post("/api/user", json=new_user)

    # Assert that the user was created and the JWT token was returned
    assert client_res.status_code == 200
    assert "access_token" in client_res.json()
    assert client_res.json()["access_token"] != ""


def test_user_login_and_gets_new_jwt(client: TestClient):
    """Test that a user can login and get a JWT token."""
    # Register a user
    new_user: dict[str, str] = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    registration_res = client.post("/api/user", json=new_user)

    reg_token = registration_res.json()["access_token"]

    # apparently the same JWT token is returned if the user registers and logs in within 0.4 seconds
    time.sleep(0.4)

    # login user
    client_res = client.post("/api/user", json=new_user)

    # if a user registers and then logs in, they should not get the same JWT token
    assert client_res.status_code == 200
    assert "access_token" in client_res.json()
    assert client_res.json()["access_token"] != reg_token
