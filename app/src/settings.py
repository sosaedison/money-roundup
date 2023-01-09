import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")
    ENV: str = os.getenv("ENV", "TEST")
    DB_CONNECTION_STRING: str = "sqlite:///moneyroundup.db"
    if ENV == "TEST":
        DB_CONNECTION_STRING: str = "sqlite:///test_moneyroundup.db"


settings = Settings()
