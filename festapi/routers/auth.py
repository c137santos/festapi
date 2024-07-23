from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from festapi.database import get_session
from festapi.models import User
from festapi.schemas import Token
from festapi.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])


T_Session = Annotated[Session, Depends(get_session)]
T_form_data = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_access_token(
    form_data: T_form_data,
    session: T_Session,
):
    user = session.scalar(select(User).where(User.email == form_data.username))
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data_claims={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'Bearer'}
