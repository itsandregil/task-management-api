from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import column
from sqlmodel import select

from app.api.deps import CreatorDep, CurrentUserDep, SessionDep
from app.api.params import PaginationParams
from app.models.tasks import Task, TaskCreate, TaskPublic, TaskUpdate
from app.models.utils import Message

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskPublic])
def get_all_tasks(
    session: SessionDep, user: CurrentUserDep, p: Annotated[PaginationParams, Depends()]
):
    """Get all personal tasks"""
    statement = (
        select(Task)
        .where(Task.creator_id == user.id, column("project_id").is_(None))
        .offset(p.offset)
        .limit(p.limit)
    )
    tasks = session.exec(statement).all()
    return tasks


@router.post("/", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_new_task(session: SessionDep, user: CurrentUserDep, task_in: TaskCreate):
    """Create a new personal task"""
    new_task = Task.model_validate(task_in, update={"creator_id": user.id})
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.patch("/{task_id}", response_model=TaskPublic)
def update_task(
    session: SessionDep,
    task: CreatorDep,
    task_in: TaskUpdate,
):
    """Update a personal task"""
    task_data = task_in.model_dump(exclude_unset=True)
    new_task = task.sqlmodel_update(task_data)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


@router.delete("/{task_id}")
def delete_task(session: SessionDep, task: CreatorDep) -> Message:
    session.delete(task)
    session.commit()
    return Message(message="task deleted successfully")
