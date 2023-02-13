from typing import Any, Generator

from fastapi import HTTPException, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.orm import Session

from moneyroundup.database import SessionLocal
from moneyroundup.settings import settings


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


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
