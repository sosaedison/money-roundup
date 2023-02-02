import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "MONEY_ROUND_UP")

    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")

    FETCH_TRANSACTIONS_INTERVAL: str = os.getenv("FETCH_TRANSACTIONS_INTERVAL", "10")

    RABBIT_HOST = os.getenv("RABBIT_HOST", "127.0.0.1")
    RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "transactions_summary")

    DB_CONNECTION_STRING: str = "sqlite:///moneyroundup.db"
    DB_ECHO: bool = False

    ENV: str = os.getenv("ENV", "DEV")
    if ENV == "TEST":
        DB_CONNECTION_STRING: str = "sqlite:///test_moneyroundup.db"


settings = Settings()
