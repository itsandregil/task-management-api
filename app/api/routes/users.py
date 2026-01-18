from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import CurrentUserDep, SessionDep
from app.core.security import create_password_hash, verify_password_hash
from app.models.users import UserCreate, UserPublic, UserUpdateMe
from app.models.utils import Message, PasswordUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserPublic)
def get_user_profile(user: CurrentUserDep):
    """Get own profile."""
    return user


@router.post("/signup", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):
    """Register a new user."""
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    user = crud.create_user(session=session, user_create=user_in)
    return user


@router.put("/me/password")
def update_user_password(
    session: SessionDep, user: CurrentUserDep, body: PasswordUpdate
) -> Message:
    """Update own password."""
    if not verify_password_hash(body.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=400,
            detail="New password cannot equal to the current password",
        )
    new_hashed_password = create_password_hash(body.new_password)
    user.hashed_password = new_hashed_password
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")


@router.patch("/me", response_model=UserPublic)
def update_user_profile(
    session: SessionDep, user: CurrentUserDep, user_in: UserUpdateMe
):
    """Update user's own profile."""
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
    """Delete user's own profile."""
    session.delete(user)
    session.commit()
    return Message(message="User deleted successfully")
