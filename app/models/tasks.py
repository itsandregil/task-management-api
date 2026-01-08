import uuid
from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel

from .projects import Project


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


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
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")

    project: Project | None = Relationship(back_populates="tasks")
