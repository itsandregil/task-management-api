"""Dependecies to be injected within API endpoints"""

# TODO: create the oauth2 scheme for a password "flow"
# TODO: create the dependency to get the authenticated user
# TODO: use the oauth form to get the client "username" and "password" as a dependency in the path operation

from typing import Annotated, Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine
from app.core.security import ALGORITHM
from app.models.users import User
from app.models.utils import TokenPayload

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/access-token")


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(oauth_scheme)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Could not be authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
