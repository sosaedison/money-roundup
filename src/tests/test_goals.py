from typing import Any, AsyncGenerator

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
async def test_create_goal(
    async_client: AsyncClient,
    create_new_user_and_token: AsyncGenerator[tuple[dict[str, str | bool], str], Any],
):
    """Test that a user can create a goal."""
    create_new_user, token = create_new_user_and_token  # type: ignore
    new_goal = {
        "user_id": create_new_user["id"],  # type: ignore
        "goal": {"category": "gas", "limit": 50},
    }

    res = await async_client.post(
        "/api/goal", json=new_goal, headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201


@pytest.mark.asyncio
async def test_get_goals(
    async_client: AsyncClient,
    create_new_user_and_token: AsyncGenerator[tuple[dict[str, str | bool], str], Any],
):
    """Test that a user can create a goal and get that goal."""
    create_new_user, token = create_new_user_and_token  # type: ignore
    new_goal = {
        "user_id": create_new_user["id"],  # type: ignore
        "goal": {"category": "gas", "limit": 50},
    }

    res = await async_client.post(
        "/api/goal", json=new_goal, headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201
    created_goal = res.json()
    assert created_goal["goal_created"] is True
    assert created_goal["id"] is not None

    res = await async_client.get(
        "/api/goal", headers={"Authorization": f"Bearer {token}"}
    )

    expected = {"goals": [{"id": created_goal["id"], "goal": new_goal["goal"]}]}
    assert res.status_code == 200
    assert res.json() == expected


@pytest.mark.asyncio
async def test_edit_goal(
    async_client: AsyncClient,
    create_new_user_and_token: AsyncGenerator[tuple[dict[str, str | bool], str], Any],
):
    """Test that a user can create a goal and get that goal."""
    create_new_user, token = create_new_user_and_token  # type: ignore

    new_goal = {
        "user_id": create_new_user["id"],  # type: ignore
        "goal": {"category": "gas", "limit": 50},
    }

    res = await async_client.post(
        "/api/goal", json=new_goal, headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201
    created_goal = res.json()
    assert created_goal["goal_created"] is True
    assert created_goal["id"] is not None

    goal_with_edits = {
        "id": created_goal["id"],  # type: ignore
        "goal": {"category": "gas", "limit": 100},
    }
    res = await async_client.patch(
        f"/api/goal/{created_goal['id']}",
        json=goal_with_edits,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200
    edited_goal = res.json()
    assert edited_goal["id"] is not None
    assert edited_goal["id"] == created_goal["id"]
    assert edited_goal["goal"] == goal_with_edits["goal"]


@pytest.mark.asyncio
async def test_delete_goal(
    async_client: AsyncClient,
    create_new_user_and_token: AsyncGenerator[tuple[dict[str, str | bool], str], Any],
):
    """Test that a user can create a goal and get that goal."""
    create_new_user, token = create_new_user_and_token  # type: ignore

    new_goal = {
        "user_id": create_new_user["id"],  # type: ignore
        "goal": {"category": "gas", "limit": 50},
    }

    res = await async_client.post(
        "/api/goal", json=new_goal, headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 201
    created_goal = res.json()
    assert created_goal["goal_created"] is True
    assert created_goal["id"] is not None

    res = await async_client.delete(
        f"/api/goal/{created_goal['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert res.status_code == 200

    res = await async_client.get(
        "/api/goal", headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json() == {"goals": []}
