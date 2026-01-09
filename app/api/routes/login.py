"""Authentication endpoints"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import SessionDep
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = crud.authenticate(
        session=session,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            details="Incorrect username or password",
            headers={"WWW-Authenticated": "Bearer"},
        )
    access_token_expire = timedelta(minutes=15)  # TODO: create this with settings
    access_token = create_access_token({"sub": user.email}, access_token_expire)
    return {"access_token": access_token, "token_type": "bearer"}
