import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "MONEY_ROUND_UP")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_KEY")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 30))

    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")

    FETCH_TRANSACTIONS_INTERVAL: str = os.getenv("FETCH_TRANSACTIONS_INTERVAL", "10")

    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "transactions_summary")

    DB_CONNECTION_STRING: str = "sqlite:///moneyroundup.db"
    DB_CONNECTION_STRING_ASYNC: str = "sqlite+aiosqlite:///moneyroundup.db"
    DB_ECHO: bool = False

    ENV: str = os.getenv("ENV", "DEV")
    if ENV == "TEST":
        DB_CONNECTION_STRING: str = "sqlite:///test_moneyroundup.db"
        DB_CONNECTION_STRING_ASYNC: str = (
            "sqlite+aiosqlite:///test_async__moneyroundup.db"
        )


settings = Settings()
