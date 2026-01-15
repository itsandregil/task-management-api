from fastapi import APIRouter

from app.models.tasks import TaskCreate, TaskPublic

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
def get_all_tasks():
    """Get tasks"""
    pass


@router.post("/", response_model=TaskPublic)
def create_new_task(task: TaskCreate):
    pass


@router.path("/{task_id}")
def update_task():
    pass


@router.delete("/{task_id}")
def delete_task():
    pass
