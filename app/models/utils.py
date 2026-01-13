from uuid import UUID

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: UUID


class Message(BaseModel):
    message: str


class PasswordUpdate(BaseModel):
    current_password: str = Field(min_length=8, max_length=50)
    new_password: str = Field(min_length=8, max_length=50)
