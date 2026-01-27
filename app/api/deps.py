from typing import Annotated, Generator
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine
from app.core.security import ALGORITHM
from app.models.projects import Project, ProjectUserLink
from app.models.tasks import Task
from app.models.users import User
from app.models.utils import TokenPayload

oauth_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/access-token")


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


def get_project_if_owner(
    project_id: UUID, session: SessionDep, user: CurrentUserDep
) -> Project:
    link = session.get(ProjectUserLink, (user.id, project_id))
    if not link:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if not link.is_owner:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return link.project


def get_task_if_creator(
    task_id: UUID, session: SessionDep, user: CurrentUserDep
) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    if task.creator_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot update this task",
        )
    return task


OwnerDep = Annotated[Project, Depends(get_project_if_owner)]
CreatorDep = Annotated[Task, Depends(get_task_if_creator)]
