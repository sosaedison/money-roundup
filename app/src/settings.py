import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PLAID_SANDBOX_KEY: str = os.environ.get("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.environ.get("PLAID_CLIENT_ID", "")
    DB_CONNECTION_STRING: str = os.environ.get(
        "DB_CONNECTION_STRING", "sqlite:///:memory"
    )


settings = Settings()
