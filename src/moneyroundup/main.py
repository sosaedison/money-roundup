from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from moneyroundup import setup_app
from moneyroundup.api import api
from moneyroundup.database import User, create_db_and_tables, drop_db_and_tables
from moneyroundup.settings import settings
from moneyroundup.users import (
    auth_backend,
    current_active_user,
    fastapi_users,
    google_oauth_client,
)

# Initialize application deps like RabbitMQ
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
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

# Add Routers to Main FastAPI App
app.include_router(api.api_router, prefix="/api")

# status check stub for health checks
@app.get("/api/status")
def home():
    return {"online": True}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    print("Starting up...")
    # Not needed if you setup a migration system like Alembic
    await drop_db_and_tables()
    await create_db_and_tables()
