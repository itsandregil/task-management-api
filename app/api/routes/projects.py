import uuid

from fastapi import APIRouter

from app.api.deps import CurrentUserDep
from app.models.projects import Project

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/")
def get_projects(current_user: CurrentUserDep) -> list[Project]:
    return current_user.project_links


@router.post("/")
def create_new_project():
    pass


@router.patch("/{project_id}")
def update_project(project_id: uuid.UUID):
    pass


@router.delete("/{project_id}")
def delete_project(project_id: uuid.UUID):
    pass
