from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from moneyroundup.settings import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    pass


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


engine = create_engine(settings.DB_CONNECTION_STRING, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

async_engine = create_async_engine(
    settings.DB_CONNECTION_STRING_ASYNC, echo=settings.DB_ECHO
)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@asynccontextmanager
async def get_async_session_context_manager() -> AsyncGenerator[Any, Any]:
    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
