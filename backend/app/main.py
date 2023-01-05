from apscheduler.schedulers.background import BackgroundScheduler

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import token, user, account, item

from base import Base  # Base for models to inherit from
from database import engine  # Engine to connect to the database

from fetch_transactions import fetch_transactions

# Recreate the database on app reload
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_transactions, "interval", seconds=10)
scheduler.start()

# Init the FastAPI app instance
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Routers to Main FastAPI App
app.include_router(token.router)
app.include_router(user.router)
app.include_router(account.router)
app.include_router(item.router)


@app.get("/")
def home():
    return {"online": True}
