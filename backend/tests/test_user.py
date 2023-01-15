from fastapi.testclient import TestClient
from src.schemas import NewUser, LoggedInUser

def test_user_registration(client: TestClient):

    new_user: NewUser = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    res = client.post("/user", json=new_user)

    res: LoggedInUser = res.json()

    assert "user_id" in list(res.keys())


def test_user_login(client: TestClient):

    new_user: NewUser = {
        "email": "sosarocks@test.com",
        "first_name": "Sosa",
        "last_name": "Rocks",
        "profile_pic_url": "http://www.some_cool_pic.com",
    }

    res = client.post("/user", json=new_user)

    res: LoggedInUser = res.json()

    new_user_id = res["user_id"]

    assert "user_id" in list(res.keys())  # successful registration

    res = client.post("/user", json=res)

    res = res.json()

    assert res["user_id"] == new_user_id  # successful login
