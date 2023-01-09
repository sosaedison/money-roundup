from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.src.settings import settings

engine = create_engine(settings.DB_CONNECTION_STRING, echo=True)
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)
