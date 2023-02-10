from fastapi import APIRouter

from moneyroundup.routers import account, item, token, user

api_router = APIRouter()

api_router.include_router(token.router)
api_router.include_router(user.router)
api_router.include_router(account.router)
api_router.include_router(item.router)
