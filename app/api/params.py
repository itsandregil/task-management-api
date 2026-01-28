"""Params for filtering and sorting and pagination"""

from pydantic import BaseModel, Field

from app.models.tasks import TaskPriority, TaskStatus


class PaginationParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(100, ge=0, le=100)


class TasksFilters(BaseModel):
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
