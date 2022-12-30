from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

engine = create_engine(settings.DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)
