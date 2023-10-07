from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from moneyroundup import setup_app
from moneyroundup.api.api import api_router
from moneyroundup.database import create_db_and_tables, drop_db_and_tables
from moneyroundup.dependencies import _get_secret_value
from moneyroundup.settings import get_settings

settings = get_settings()

# setup_app()

# Init the FastAPI app instance
app = FastAPI(title=settings.PROJECT_TITLE)

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
def home():
    return {
        "online": True,
        "status": "OK",
        "message": "Hello World",
        "settings": settings.dict(),
    }


@app.on_event("startup")
async def on_startup():
    print("Recreating database tables")
    # Not needed if you setup a migration system like Alembic
    await drop_db_and_tables()
    await create_db_and_tables()
