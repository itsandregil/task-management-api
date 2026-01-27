import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from .projects import ProjectUserLink
from .tasks import Task


class UserBase(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserPublic(UserBase):
    id: uuid.UUID


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str

    tasks: list[Task] = Relationship(back_populates="creator")
    project_links: list[ProjectUserLink] = Relationship(back_populates="user")
