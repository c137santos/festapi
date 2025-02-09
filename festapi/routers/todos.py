from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from festapi.database import get_session
from festapi.models import Todo, TodoState, User
from festapi.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from festapi.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

T_Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    user: CurrentUser,
    session: T_Session,
):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


@router.get('/', response_model=TodoList)
def list_todos(
    session: T_Session,
    user: CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: TodoState | None = None,
    offset: str | None = None,
    limit: int | None = None,
):
    query = select(Todo).where(Todo.user_id == user.id)
    if title:
        query = query.filter(Todo.title.contains(title))
        # Pode com filtro, e pode com where
    if description:
        query = query.filter(Todo.description.contains(description))
    if state:
        query = query.filter(Todo.state == state)
    todos = session.scalars(query.offset(offset).limit(limit)).all()
    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: CurrentUser):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=TodoPublic)
def patch_todo(
    todo_id: int, session: T_Session, user: CurrentUser, todo: TodoUpdate
):
    db_todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id, Todo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
