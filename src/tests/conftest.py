import os

from fastapi.testclient import TestClient
from pytest import fixture

os.environ["ENV"] = "TEST"

from moneyroundup.main import app
from moneyroundup.settings import settings


@fixture
def client():
    client = TestClient(app)
    yield client


def decode_token(token: str) -> str:
    from jose import jwt

    return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)[
        "sub"
    ]
