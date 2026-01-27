import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .projects import Project, ProjectPublic

if TYPE_CHECKING:
    from .users import User


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    priority: TaskPriority | None = Field(default=None)
    due_date: datetime | None = Field(default=None)


class TaskPublic(TaskBase):
    id: uuid.UUID
    status: TaskStatus
    created_at: datetime


class TaskCreate(TaskBase):
    project_id: uuid.UUID | None = None


class TaskUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.TODO)

    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    creator_id: uuid.UUID = Field(nullable=False, foreign_key="user.id")
    project_id: uuid.UUID | None = Field(default=None, foreign_key="project.id")

    project: Project | None = Relationship(back_populates="tasks")
    creator: "User" = Relationship(back_populates="tasks")


class ProjectWithTasks(ProjectPublic):
    tasks: list[TaskPublic] = []
