"""Dependecies to be injected within API endpoints"""

# TODO: create the oauth2 scheme for a password "flow"
# TODO: create the dependency to get the authenticated user
# TODO: use the oauth form to get the client "username" and "password" as a dependency in the path operation

from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
