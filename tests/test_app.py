from http import HTTPStatus


def test_read_root_suscess(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert 'Hello World' in response.text
