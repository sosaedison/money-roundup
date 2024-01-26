from fastapi import APIRouter
from moneyroundup.routers import account, auth, goals, item, token

api_router = APIRouter()

api_router.include_router(token.router)
api_router.include_router(account.router)
api_router.include_router(item.router)
api_router.include_router(auth.router)
api_router.include_router(goals.router)
