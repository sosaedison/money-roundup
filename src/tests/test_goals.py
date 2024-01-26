from typing import Any, AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient

from moneyroundup.database import create_db_and_tables, drop_db_and_tables


@pytest_asyncio.fixture(scope="function", autouse=True)
async def rest_db():
    """Reset the database before each test."""
    await drop_db_and_tables()
    await create_db_and_tables()

def test_create_goal(async_client: AsyncClient, create_new_user: AsyncGenerator[Any, Any]):
    print(create_new_user)