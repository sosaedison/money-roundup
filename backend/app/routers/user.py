from uuid import uuid4
from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError as SQAIntegrityError

from models import User
from dependencies import get_db  # Dependency for access to the database

from pydantic import BaseModel

class NewUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_pic_url: str | None = None

router = APIRouter(prefix="/user", tags=["User"])

@router.post("")
def register(new_user: NewUser, session: Session = Depends(get_db)):
    try:
        u = User(id=str(uuid4()),**new_user.dict())
        with session.begin():
            session.add(u)
            session.commit()

    except (IntegrityError, SQAIntegrityError) as ex:
        pass

    return new_user.dict()
