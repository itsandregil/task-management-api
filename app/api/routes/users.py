from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import CurrentUserDep, SessionDep
from app.models.users import UserCreate, UserPublic, UserUpdateMe
from app.models.utils import Message

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.put("/me", response_model=UserPublic)
def update_user_profile(
    session: SessionDep, user: CurrentUserDep, user_in: UserUpdateMe
):
    if user_in.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="User with this email already exists",
            )
    user_data = user_in.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.delete("/me", response_model=Message)
def delete_user(session: SessionDep, user: CurrentUserDep):
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
