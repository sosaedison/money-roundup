import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")
    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_QUEUE = os.getenv("RABBIT_QUEUE", "transactions_summary")
    ENV: str = os.getenv("ENV", "DEV")
    DB_CONNECTION_STRING: str = "sqlite:///moneyroundup.db"
    DB_ECHO: bool = False
    if ENV == "TEST":
        DB_CONNECTION_STRING: str = "sqlite:///test_moneyroundup.db"


settings = Settings()
