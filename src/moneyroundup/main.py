from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from moneyroundup.api.api import api_router
from moneyroundup.settings import settings

app = FastAPI(title=settings.PROJECT_TITLE)

origins = [
    settings.FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def home():
    return {"online": True}
