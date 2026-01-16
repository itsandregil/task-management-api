from uuid import UUID

from app.models.tasks import Task


def is_task_creator(*, task: Task, user_id: UUID) -> bool:
    return task.creator_id == user_id
