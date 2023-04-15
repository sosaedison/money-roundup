from fastapi import APIRouter

from moneyroundup import settings
from moneyroundup.schemas import UserCreate, UserRead, UserUpdate
from moneyroundup.users import auth_backend, fastapi_users, google_oauth_client

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/jwt")
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users"
)
router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        settings.SECRET_KEY,
        is_verified_by_default=True,
    ),
    prefix="/google",
)
