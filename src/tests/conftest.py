from fastapi.testclient import TestClient
from pytest import fixture

import os

os.environ["ENV"] = "TEST"

from moneyroundup.main import app


@fixture
def client():
    client = TestClient(app)
    yield client
