import pytest
from fastapi.testclient import TestClient

from festapi.app import app


@pytest.fixture()
def client():
    return TestClient(app)
