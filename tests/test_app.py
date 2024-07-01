from http import HTTPStatus


def test_read_root_suscess(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert 'Hello World' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testeusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )
    # Validar UserPublic
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testeusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'testeusername', 'email': 'test@test.com', 'id': 1}
        ]
    }


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testeusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_get_user_not_found(client):
    response = client.get('/users/555')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': '',
            'username': 'mudouONome',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'mudouONome',
        'email': 'test@test.com',
        'id': 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        '/users/5555',
        json={
            'password': '',
            'username': 'mudouONome',
            'email': 'test@test.com',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/5555')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'User not found'
