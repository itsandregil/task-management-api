import uuid
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Project(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))


class Task(SQLModel, table=True):
    pass


class User(SQLModel, table=True):
    pass
