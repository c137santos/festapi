from http import HTTPStatus

from fastapi.testclient import TestClient

from festapi.app import app

client = TestClient(app)


def test_read_root_suscess():
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert 'Hello World' in response.text
