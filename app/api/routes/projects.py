from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, HTTPException, status

from app import crud
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
def get_project(project_id: UUID, session: SessionDep, user: CurrentUserDep):
    link = session.get(ProjectUserLink, {"user_id": user.id, "project_id": project_id})
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return link.project


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


# TODO: Make this sending invitation via email using google's smtp server (like IRL)
@router.post("/{project_id}/invite")
def add_new_member(
    session: SessionDep, project: OwnerDep, member_email: Annotated[str, Body()]
) -> Message:
    user = crud.get_user_by_email(session=session, email=member_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    new_member = ProjectUserLink(project_id=project.id, user_id=user.id)
    session.add(new_member)
    session.commit()
    session.refresh(new_member)
    return Message(message="Member added correctly")
