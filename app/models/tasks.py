import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .projects import Project

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


class TaskUserLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id", primary_key=True)
    task_id: uuid.UUID = Field(default=None, foreign_key="task.id", primary_key=True)


class Task(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str | None = Field(default=None, max_length=255)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority | None = Field(default=None)
    due_date: datetime | None = Field(default=None)
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    project_id: uuid.UUID = Field(default=None, foreign_key="project.id")

    project: Project | None = Relationship(back_populates="tasks")
    users: list["User"] = Relationship(
        back_populates="tasks",
        link_model=TaskUserLink,
    )
