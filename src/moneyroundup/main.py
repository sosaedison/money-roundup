from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from moneyroundup.api.api import api_router
from moneyroundup.database import create_db_and_tables, drop_db_and_tables
from moneyroundup.dependencies import _get_secret_value
from moneyroundup.settings import get_settings

settings = get_settings()

# setup_app()
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Recreating database tables")
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield
    await drop_db_and_tables()

# Init the FastAPI app instance
app = FastAPI(title=settings.PROJECT_TITLE, lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware, secret_key=_get_secret_value(settings.APP_SECRET_KEY)
)

# Add Routers to Main FastAPI App
app.include_router(api_router, prefix="/api")


# status check stub for health checks
@app.get("/")
@app.head("/")
def home():
    return {
        "online": True,
        "status": "OK",
        "message": "Hello World",
        "settings": settings.model_dump(),
    }


