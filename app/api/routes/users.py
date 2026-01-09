from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.models.users import UserCreate, UserPublic

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
