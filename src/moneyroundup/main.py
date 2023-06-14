from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from moneyroundup import setup_app
from moneyroundup.api import api
from moneyroundup.database import create_db_and_tables, drop_db_and_tables
from moneyroundup.settings import settings

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


@app.on_event("startup")
async def on_startup():
    print("Recreating database tables")
    # Not needed if you setup a migration system like Alembic
    await drop_db_and_tables()
    await create_db_and_tables()
