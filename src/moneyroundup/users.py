import logging
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from moneyroundup.database import OAuthAccount, User, get_user_db
from moneyroundup.services.email import EmailFactory, EmailService
from moneyroundup.settings import settings

logger = logging.getLogger(__name__)

# from httpx_oauth.clients.google import GoogleOAuth2


# google_oauth_client = GoogleOAuth2(
#     settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET
# )


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_SECRET_KEY
    reset_password_token_lifetime_seconds = (
        settings.RESET_PASSWORD_TOKEN_LIFETIME_SECONDS
    )
    reset_password_token_audience = settings.RESET_PASSWORD_TOKEN_AUDIENCE

    verification_token_secret = settings.EMAIL_VERIFICATION_SECRET_KEY
    verification_token_lifetime_seconds = (
        settings.EMAIL_VERIFICATION_TOKEN_LIFETIME_SECONDS
    )
    verification_token_audience = settings.EMAIL_VERIFICATION_TOKEN_AUDIENCE

    email_service: EmailService = EmailFactory(env=settings.EMAIL_SERVICE_TYPE)

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        welcome_email_text = f"""Welcome to Money Roundup,{user.first_name}! \n\n You can expect a follow up email from us to verify your email.\n\n Please verify your email so you can receive your daily spending notices! 🙃"""
        subject = "Welcome to Money Roundup!"
        try:
            self.email_service.send_email(
                to=user.email,
                subject=subject,
                body=welcome_email_text,
            )
            logger.info(f"User {user.id} has registered. Welcome email sent.")
        except Exception as e:
            logger.error(f"Error sending welcome email: {e}")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # What we'd want to do here is formulate an email to the user with a link to reset their password.

        reset_password_email_text = f"""Please reset your password by clicking the link below:\n\n{settings.LOCAL_BACKEND_URL}/auth/forgot-password?token={token}\n\nThanks!\n\nThe Money Roundup Team"""
        subject = "Reset your password with Money Roundup"

        try:
            self.email_service.send_email(
                to=user.email,
                subject=subject,
                body=reset_password_email_text,
            )
            logger.info(
                f"Password reset requested for user {user.id}. Reset email sent."
            )
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # What we'd want to do here is formulate an email to the user with a link to verify their email.

        verification_email_text = f"""Please verify your email address by clicking the link below:\n\n{settings.LOCAL_BACKEND_URL}/auth/verify?token={token}\n\n(You'll need to verify before you can receive any emails)\n\nThanks!\n\nThe Money Roundup Team"""
        subject = "Verify your email with Money Roundup"

        try:
            self.email_service.send_email(
                to=user.email,
                subject=subject,
                body=verification_email_text,
            )
            logger.info(
                f"Verification requested for user {user.id}. Verification email sent."
            )
        except Exception as e:
            logger.error(f"Error sending verification email: {e}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="/api/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.JWT_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[OAuthAccount, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
