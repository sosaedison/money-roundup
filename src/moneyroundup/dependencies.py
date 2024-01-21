import copy
from datetime import datetime, timedelta
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, Union

from fastapi import Depends, HTTPException, Request
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import SecretStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from moneyroundup.database import SessionLocal, async_session_maker
from moneyroundup.models import UserOld
from moneyroundup.schemas import UserFromDB
from moneyroundup.settings import get_settings

settings = get_settings()

SecretType = Union[str, SecretStr]


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession = async_session_maker()
    try:
        yield db
    finally:
        await db.close()


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_secret_value(secret: SecretType) -> str:
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


def generate_jwt(
    payload: dict,
    expires_delta: Optional[int] = None,
    secret: SecretType = settings.APP_SECRET_KEY,
):
    payload = copy.deepcopy(payload)

    now = datetime.utcnow()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        payload.update({"exp": expire})

    payload.update({"iat": now})

    return jwt.encode(
        payload,
        get_secret_value(secret),
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_jwt(
    encoded_jwt: str,
    secret: SecretType,
    audience: str,
    algorithms: List[str] = [settings.JWT_ALGORITHM],
) -> Dict[str, Any]:
    return jwt.decode(
        encoded_jwt,
        get_secret_value(secret),
        audience=audience,
        algorithms=algorithms,
    )


def validate_creds(request: Request) -> dict[str, Any] | None:
    """Validate the JWT token in the Authorization header."""
    try:
        auth = request.headers["Authorization"]
        if auth.startswith("Bearer "):
            token = auth[7:]
            return jwt.decode(
                token,
                get_secret_value(settings.APP_SECRET_KEY),
                algorithms=[settings.JWT_ALGORITHM],
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
        user = session.query(UserOld).get(token["sub"])

    return UserFromDB.from_orm(user)
