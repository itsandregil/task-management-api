import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from .users import User

if TYPE_CHECKING:
    from .tasks import Task


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")

    tasks: list["Task"] | None = Relationship(back_populates="project")
    user: User = Relationship(back_populates="projects")
