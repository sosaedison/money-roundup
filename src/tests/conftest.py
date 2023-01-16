from fastapi.testclient import TestClient
from pytest import fixture

from moneyroundup.main import app


@fixture
def client():
    client = TestClient(app)
    yield client
