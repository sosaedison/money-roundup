import pytest
import pytest_asyncio
from httpx import AsyncClient

from moneyroundup.database import create_db_and_tables, drop_db_and_tables


@pytest_asyncio.fixture(scope="function", autouse=True)
async def rest_db():
    """Reset the database before each test."""
    await drop_db_and_tables()
    await create_db_and_tables()


@pytest.mark.asyncio
async def test_user_register_and_access_their_info(async_client: AsyncClient):
    """Test that a user can register and get a JWT token and then use that token to access their info."""

    # define a user
    new_user: dict[str, str] = {"email": "sosarocks@test.com", "password": "Sosa"}

    # register the user
    client_res = await async_client.post("/api/auth/register", json=new_user)

    # assert that the user was created
    assert client_res.status_code == 201

    # login with the new user
    client_res = await async_client.post(
        "/api/auth/jwt/login",
        data={"username": new_user["email"], "password": new_user["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert client_res.status_code == 200

    # get the access token
    access_token = client_res.json()["access_token"]

    # get the user from the database
    client_res = await async_client.get(
        f"/api/auth/users/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    registered_user = client_res.json()

    assert registered_user["email"] == new_user["email"]
