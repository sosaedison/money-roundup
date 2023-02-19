import copy
from datetime import datetime, timedelta
from sqlite3 import IntegrityError as SQLiteIntegrityError
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends
from jose import jwt
from sqlalchemy.exc import IntegrityError as SQAIntegrityError
from sqlalchemy.orm import Session

from moneyroundup.dependencies import get_db
from moneyroundup.models import User
from moneyroundup.schemas import LoggedInUser, NewUser
from moneyroundup.settings import settings

router = APIRouter(prefix="/user", tags=["User"])


def generate_jwt(data: dict | None = None, expires_delta: timedelta | None = None):
    if data is None:
        data = {}

    to_encode = copy.deepcopy(data)

    now = datetime.utcnow()
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    to_encode.update({"iat": now})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


@router.post("", response_model=LoggedInUser)
def register(
    new_user: NewUser,
    session: Session = Depends(get_db),
):
    """Register a new user if the user email doesn't exist. Otherwise return the user."""
    try:

        u = User(id=str(uuid4()), **new_user.dict())
        with session.begin():
            session.add(u)
            session.commit()

    except (
        SQLiteIntegrityError,
        SQAIntegrityError,
    ):  # A user with this email already exists
        with session.begin():
            u: Any = session.query(User).filter(User.email == new_user.email).first()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    access_token = generate_jwt({"sub": u.id}, expires_delta=access_token_expires)

    return {
        "first_name": u.first_name,
        "last_name": u.last_name,
        "email": u.email,
        "profile_pic_url": u.profile_pic_url,
        "access_token": access_token,
    }
