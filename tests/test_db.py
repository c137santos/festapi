from sqlalchemy import select

from festapi.models import Todo, User


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


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos
