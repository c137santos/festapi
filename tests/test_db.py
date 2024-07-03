from sqlalchemy import select

from festapi.models import User


def test_create_user(session):
    user = User(username='Santos', password='senha', email='mail@gmail.com')
    session.add(user)
    session.commit()
    session.refresh(user)

    result = session.scalar(select(User).where(User.email == 'mail@gmail.com'))

    assert result.id == 1
    assert result.username == 'Santos'
    assert result.password == 'senha'
    assert result.email == 'mail@gmail.com'
