from typing import Any, Generator

from fastapi import Depends, HTTPException, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from moneyroundup.database import SessionLocal
from moneyroundup.models import User
from moneyroundup.schemas import UserFromDB
from moneyroundup.settings import settings


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_creds(request: Request) -> dict[str, Any] | None:
    """Validate the JWT token in the Authorization header."""
    try:
        auth = request.headers["Authorization"]
        if auth.startswith("Bearer "):
            token = auth[7:]
            return jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
    except KeyError:
        raise HTTPException(status_code=401, detail="No token provided")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")


def get_current_user(
    token: dict[str, Any] | None = Depends(validate_creds),
    session: Session = Depends(get_db),
) -> UserFromDB:
    """Get the current user from the JWT token."""
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    with session.begin():
        user = session.query(User).get(token["sub"])

    return UserFromDB.from_orm(user)
