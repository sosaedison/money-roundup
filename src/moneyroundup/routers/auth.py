import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from moneyroundup import settings
from moneyroundup.database import User, get_async_session_context_manager
from moneyroundup.dependencies import decode_jwt
from moneyroundup.schemas import UserCreate, UserRead, UserUpdate
from moneyroundup.users import auth_backend, fastapi_users

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt")
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users"
)
# router.include_router(
#     fastapi_users.get_oauth_router(
#         google_oauth_client,
#         auth_backend,
#         settings.APP_SECRET_KEY,
#         is_verified_by_default=True,
#     ),
#     prefix="/google",
# )


async def validate_token_on_verify(request: Request) -> dict | None:
    """Validate the token in the request and return it if valid"""
    token = request.query_params.get("token")
    if not token:
        return None

    try:
        payload = decode_jwt(
            encoded_jwt=token,
            secret=settings.EMAIL_VERIFICATION_SECRET_KEY,
            audience=settings.EMAIL_VERIFICATION_TOKEN_AUDIENCE,
        )
    except ExpiredSignatureError:
        logger.error("Token expired")
        return None
    except JWTError as jwt_error:
        logger.warning(
            f"Could not validate token for some reason other than expiration: {jwt_error}"
        )
        return None

    return payload


async def validate_token_on_password_reset(request: Request) -> dict | None:
    """Validate the token in the request and return it if valid"""
    token = request.query_params.get("token")
    if not token:
        return None

    try:
        payload = decode_jwt(
            encoded_jwt=token,
            secret=settings.RESET_PASSWORD_SECRET_KEY,
            audience=settings.RESET_PASSWORD_TOKEN_AUDIENCE,
        )
    except ExpiredSignatureError:
        logger.info("Token expired")
        return None
    except JWTError as jwt_error:
        logger.warning(
            f"Could not validate token for some reason other than expiration: {jwt_error}"
        )
        return None

    return payload


@router.get("/verify")
async def verify(
    payload: dict | None = Depends(validate_token_on_verify),
    async_db_session: AsyncSession = Depends(get_async_session_context_manager),
):
    """
    Given a valid jwt token, set the user email to verified.

    Technically, this endpoint is not necessary. Fastapi-users has a built in endpoint for verifying emails but that endpoint takes a token in the body of the request. I needed to use a query parameter instead. This endpoint is a copy of the fastapi-users endpoint with the token validation logic changed to use a query parameter instead of a body parameter.
    """
    if not payload:
        return RedirectResponse(
            url=f"{settings.EMAIL_VERIFICATION_REDIRECT_URL}/verification-error",
            status_code=308,
        )

    async with async_db_session as session:
        redirect_url = settings.EMAIL_VERIFICATION_REDIRECT_URL

        try:
            user = await session.execute(select(User).where(User.id == payload["sub"]))
            user = user.scalars().first()
            if user:
                logger.info(f"User {user.id} has verified their email address")
                user.is_verified = True
                await session.commit()
        except Exception as e:
            logger.error(f"Error verifying user email: {e}")
            return RedirectResponse(
                url=f"{redirect_url}/verification-error",
                status_code=308,
            )

    return RedirectResponse(
        url=f"{redirect_url}/verification-success",
        status_code=308,
    )


@router.get("/forgot-password")
async def forgot_password(
    request: Request,
    payload: dict | None = Depends(validate_token_on_password_reset),
):
    """
    Given a valid jwt token, redirect the user to the forgot password page.
    """
    redirect_url = settings.FORGOT_PASSWORD_REDIRECT_URL

    if not payload:
        return RedirectResponse(
            url=f"{redirect_url}?error=true",
            status_code=308,
        )

    token = request.query_params.get("token")

    return RedirectResponse(
        url=f"{redirect_url}?token={token}",
        status_code=308,
    )
