import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "MONEY_ROUND_UP")

    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")

    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    FETCH_TRANSACTIONS_INTERVAL: str = os.getenv("FETCH_TRANSACTIONS_INTERVAL", "10")

    ENV: str = os.getenv("ENV", "DEV")


settings = Settings()
