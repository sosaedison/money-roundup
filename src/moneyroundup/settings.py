import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr

load_dotenv()

PRODUCTION_BASE_URL = "https://moneyroundup.com"


class Settings(BaseSettings):
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "MONEY_ROUND_UP")
    LOCAL_FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    LOCAL_BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000/api")
    LOCAL_EMAIL_VERIFICATION_REDIRECT_URL: str = "http://localhost:3000"
    PRODUCTION_EMAIL_VERIFICATION_REDIRECT_URL: str = os.getenv(
        "PRODUCTION_EMAIL_VERIFICATION_REDIRECT_URL", "https://localhost:3000"
    )
    LOCAL_FORGOT_PASSWORD_REDIRECT_URL: str = "http://localhost:3000/forgot-password"
    PRODUCTION_FORGOT_PASSWORD_REDIRECT_URL: str = os.getenv(
        "PRODUCTION_FORGOT_PASSWORD_REDIRECT_URL", ""
    )
    APP_SECRET_KEY: SecretStr = SecretStr(
        os.getenv("APP_SECRET_KEY", "SUPER_SECRET_KEY")
    )

    EMAIL_SERVICE_USERNAME: str = os.getenv("EMAIL_SERVICE_USERNAME", "")
    EMAIL_SERVICE_PASSWORD: SecretStr = SecretStr(
        os.getenv("EMAIL_SERVICE_PASSWORD", "")
    )
    EMAIL_SERVICE_HOST: str = os.getenv("EMAIL_SERVICE_HOST", "smtp.gmail.com")
    EMAIL_SERVICE_PORT: int = int(os.getenv("EMAIL_SERVICE_PORT", 587))
    EMAIL_SERVICE_TYPE: str = os.getenv("EMAIL_SERVICE_TYPE", "DEV")

    RESET_PASSWORD_SECRET_KEY: SecretStr = SecretStr(
        os.getenv("RESET_PASSWORD_SECRET_KEY", "SUPER_SECRET_KEY")
    )
    RESET_PASSWORD_TOKEN_LIFETIME_SECONDS: int = int(
        os.getenv("RESET_PASSWORD_TOKEN_LIFETIME_SECONDS", 600)
    )
    RESET_PASSWORD_TOKEN_AUDIENCE: str = os.getenv(
        "RESET_PASSWORD_TOKEN_AUDIENCE", "moneyroundup:reset"
    )

    EMAIL_VERIFICATION_SECRET_KEY: SecretStr = SecretStr(
        os.getenv("EMAIL_VERIFICATION_SECRET_KEY", "SUPER_SECRET_KEY")
    )
    EMAIL_VERIFICATION_TOKEN_LIFETIME_SECONDS: int = int(
        os.getenv("EMAIL_VERIFICATION_TOKEN_LIFETIME_SECONDS", 3)
    )
    EMAIL_VERIFICATION_TOKEN_AUDIENCE: str = os.getenv(
        "EMAIL_VERIFICATION_TOKEN_AUDIENCE", "moneyroundup:verify"
    )

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_SECRET: SecretStr = SecretStr(os.getenv("JWT_SECRET", "SUPER_SECRET_KEY"))
    ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 30))

    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: SecretStr = SecretStr(os.getenv("GOOGLE_CLIENT_SECRET", ""))
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")

    FETCH_TRANSACTIONS_INTERVAL: str = os.getenv("FETCH_TRANSACTIONS_INTERVAL", "10")

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
