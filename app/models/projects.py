import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .tasks import Task
    from .users import User


class ProjectUserLink(SQLModel, table=True):
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id", primary_key=True)
    project_id: uuid.UUID = Field(
        default=None, foreign_key="project.id", primary_key=True
    )
    is_owner: bool = False

    user: "User" = Relationship(back_populates="project_links")
    project: "Project" = Relationship(back_populates="user_links")


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")

    tasks: list["Task"] | None = Relationship(back_populates="project")
    user_links: list[ProjectUserLink] = Relationship(back_populates="project")
