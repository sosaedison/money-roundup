from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from moneyroundup import setup_app

from moneyroundup.api import api

from moneyroundup.base import Base  # Base for models to inherit from
from moneyroundup.database import engine  # Engine to connect to the database

from moneyroundup.settings import settings

# Initialize application deps like RabbitMQ
setup_app()

# Recreate the database on app reload
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

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

# Add Routers to Main FastAPI App
app.include_router(api.api_router, prefix="/api")


@app.get("/api/status")
def home():
    return {"online": True}
