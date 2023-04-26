import os
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

# from httpx_oauth.clients.google import GoogleOAuth2

from moneyroundup.database import OAuthAccount, get_user_db
from moneyroundup.settings import settings


# google_oauth_client = GoogleOAuth2(
#     settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET
# )


class UserManager(UUIDIDMixin, BaseUserManager[OAuthAccount, uuid.UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_SECRET_KEY
    verification_token_secret = settings.EMAIL_VERIFICATION_SECRET_KEY

    async def on_after_register(
        self, user: OAuthAccount, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: OAuthAccount, token: str, request: Optional[Request] = None
    ):
        # What we'd want to do here is formulate an email to the user with a link to reset their password.
        # For now, we'll just print the token to the console.

        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: OAuthAccount, token: str, request: Optional[Request] = None
    ):
        # What we'd want to do here is formulate an email to the user with a link to verify their email.
        # For now, we'll just print the token to the console.

        print(f"Verification requested for user {user.id}. Verification token: {token}")


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