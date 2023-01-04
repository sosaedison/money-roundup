from uuid import uuid4
from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError as SQAIntegrityError
from schemas import LoggedInUser

from models import User
from dependencies import get_db  # Dependency for access to the database

from schemas import NewUser

router = APIRouter(prefix="/user", tags=["User"])


@router.post("", response_model=LoggedInUser)
def register(new_user: NewUser, session: Session = Depends(get_db)):
    try:

        u = User(id=str(uuid4()), **new_user.dict())
        with session.begin():
            session.add(u)
            session.commit()

    except (IntegrityError, SQAIntegrityError) as ex:
        with session.begin():
            u: User = session.query(User).filter(User.email == new_user.email).first()

    return {
        "user_id": u.id,
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "profile_pic_url": u.profile_pic_url,
    }
