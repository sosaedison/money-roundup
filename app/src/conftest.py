from fastapi.testclient import TestClient
from pytest import fixture

from app.src.main import app


@fixture
def client():
    client = TestClient(app)
    yield client
