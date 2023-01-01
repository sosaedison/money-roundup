from uuid import uuid4
from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError as SQAIntegrityError

from models import User
from dependencies import get_db  # Dependency for access to the database

from schemas import NewUser

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

    return {"user_id": u.id, "first_name": u.first_name, "last_name": u.last_name, "email": u.email}
