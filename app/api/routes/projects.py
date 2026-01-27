from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUserDep, OwnerDep, SessionDep
from app.models.projects import (
    Project,
    ProjectCreate,
    ProjectPublic,
    ProjectUpdate,
    ProjectUserLink,
)
from app.models.tasks import ProjectWithTasks
from app.models.utils import Message

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[ProjectPublic])
def get_projects(user: CurrentUserDep):
    return [link.project for link in user.project_links]


@router.get("/{project_id}", response_model=ProjectWithTasks)
def get_project(project_id: UUID, session: SessionDep):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=ProjectPublic)
def create_new_project(
    session: SessionDep, user: CurrentUserDep, project_data: ProjectCreate
):
    new_project = Project.model_validate(project_data)
    project_user_link = ProjectUserLink(
        user=user,
        project=new_project,
        is_owner=True,
    )
    session.add(project_user_link)
    session.commit()
    return new_project


@router.patch("/{project_id}", response_model=ProjectPublic)
def update_project(session: SessionDep, project: OwnerDep, project_in: ProjectUpdate):
    project_data = project_in.model_dump(exclude_unset=True)
    project.sqlmodel_update(project_data)
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(session: SessionDep, project: OwnerDep) -> Message:
    session.delete(project)
    session.commit()
    return Message(message="Project deleted")
