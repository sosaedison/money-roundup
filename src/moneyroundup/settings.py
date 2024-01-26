import os

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

from moneyroundup.services.secret_manager import SecretManager

load_dotenv()


secret_manager = SecretManager()


class Settings(BaseSettings):
    """Base Settings"""

    ENV: str = os.getenv("ENV", "DEV")
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "MONEY_ROUND_UP")
    APP_SECRET_KEY: SecretStr = SecretStr(
        os.getenv("APP_SECRET_KEY", "AWSSECRET_APP_SECRET_KEY")
    )

    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8080/api")

    EMAIL_SERVICE_USERNAME: str = os.getenv("EMAIL_SERVICE_USERNAME", "")
    EMAIL_SERVICE_PASSWORD: SecretStr = SecretStr(
        os.getenv("EMAIL_SERVICE_PASSWORD", "")
    )
    EMAIL_SERVICE_HOST: str = os.getenv("EMAIL_SERVICE_HOST", "smtp.gmail.com")
    EMAIL_SERVICE_PORT: int = int(os.getenv("EMAIL_SERVICE_PORT", 587))
    EMAIL_SERVICE_TYPE: str = os.getenv("EMAIL_SERVICE_TYPE", "DEV")
    EMAIL_VERIFICATION_REDIRECT_URL: str = FRONTEND_URL
    EMAIL_VERIFICATION_SECRET_KEY: SecretStr = SecretStr(
        os.getenv(
            "EMAIL_VERIFICATION_SECRET_KEY", "AWSSECRET_EMAIL_VERIFICATION_SECRET_KEY"
        )
    )
    EMAIL_VERIFICATION_TOKEN_LIFETIME_SECONDS: int = int(
        os.getenv("EMAIL_VERIFICATION_TOKEN_LIFETIME_SECONDS", 30)
    )
    EMAIL_VERIFICATION_TOKEN_AUDIENCE: str = os.getenv(
        "EMAIL_VERIFICATION_TOKEN_AUDIENCE", "moneyroundup:verify"
    )

    FORGOT_PASSWORD_REDIRECT_URL: str = f"{FRONTEND_URL}/forgot-password"
    RESET_PASSWORD_SECRET_KEY: SecretStr = SecretStr(
        os.getenv("RESET_PASSWORD_SECRET_KEY", "AWSSECRET_FORGOT_PASSWORD_SECRET_KEY")
    )
    RESET_PASSWORD_TOKEN_LIFETIME_SECONDS: int = int(
        os.getenv("RESET_PASSWORD_TOKEN_LIFETIME_SECONDS", 600)
    )
    RESET_PASSWORD_TOKEN_AUDIENCE: str = os.getenv(
        "RESET_PASSWORD_TOKEN_AUDIENCE", "moneyroundup:reset"
    )

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_SECRET: SecretStr = SecretStr(
        os.getenv("JWT_SECRET", "AWSSECRET_JWT_SECRET_KEY")
    )
    ACCESS_TOKEN_EXPIRE_SECONDS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 30))

    PLAID_SANDBOX_KEY: str = os.getenv("PLAID_SANDBOX_KEY", "")
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: SecretStr = SecretStr(os.getenv("GOOGLE_CLIENT_SECRET", ""))
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "")

    FETCH_TRANSACTIONS_INTERVAL: int = int(
        os.getenv("FETCH_TRANSACTIONS_INTERVAL", "10")
    )

    DB_CONNECTION_STRING: str = os.getenv(
        "AWSSECRET_DB_CONNECTION_STRING", "postgresql+asyncpg://moneyroundup:password@db:5432/moneyroundup"
    )
    DB_CONNECTION_STRING_ASYNC: str = os.getenv(
        "AWSSECRET_DB_CONNECTION_STRING_ASYNC", "sqlite+aiosqlite:///moneyroundup.db"
    )
    DB_ECHO: bool = False


class DevSettings(Settings):
    """Settings for Development Environment"""


class ProdSettings(Settings):
    """Settings for Production Environment"""

    ENV: str = os.getenv("ENV", "DEV")
    if ENV == "PROD":
        LOGGING_LEVEL: str = "ERROR"
        _BASE_URL: str = os.getenv("BASE_URL", "https://moneyroundup.com")
        FRONTEND_URL: str = os.getenv("FRONTEND_URL", _BASE_URL)
        BACKEND_URL: str = os.getenv("BACKEND_URL", f"{_BASE_URL}/api")

        RESET_PASSWORD_SECRET_KEY: str | dict[str, str] = secret_manager.get_secret(
            "RESET_PASSWORD_SECRET_KEY"
        )
        EMAIL_VERIFICATION_SECRET_KEY: str | dict[str, str] = secret_manager.get_secret(
            "EMAIL_VERIFICATION_SECRET_KEY"
        )
        JWT_SECRET: str | dict[str, str] = secret_manager.get_secret("JWT_SECRET")
        DB_CONNECTION_STRING: str | dict[str, str] = secret_manager.get_secret(
            "DB_CONNECTION_STRING"
        )
        DB_CONNECTION_STRING_ASYNC: str | dict[str, str] = secret_manager.get_secret(
            "DB_CONNECTION_STRING_ASYNC"
        )
        APP_SECRET_KEY: str | dict[str, str] = secret_manager.get_secret(
            "APP_SECRET_KEY"
        )


class TestSettings(Settings):
    """Settings for Test Environment"""

    DB_CONNECTION_STRING: str = os.getenv(
        "AWSSECRET_DB_CONNECTION_STRING", "postgresql+asyncpg://moneyroundup:password@db:5432/moneyroundup"
    )
    DB_CONNECTION_STRING_ASYNC: str = os.getenv(
        "AWSSECRET_DB_CONNECTION_STRING_ASYNC", "postgresql+aiosqlite://moneyroundup:password@db:5432/moneyroundup"
    )
    DB_ECHO: bool = True


# ENV = os.getenv("ENV", "DEV")
# settings_options = {"DEV": DevSettings, "PROD": ProdSettings, "TEST": TestSettings}
# settings: Settings = settings_options.get(ENV, DevSettings)()


def get_settings() -> Settings:
    ENV: str = os.getenv("ENV", "DEV")
    settings_options = {"DEV": DevSettings, "PROD": ProdSettings, "TEST": TestSettings}
    return settings_options.get(ENV, DevSettings)()
