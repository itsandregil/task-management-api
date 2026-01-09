from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import select

from app.api.deps import SessionDep
from app.core.security import create_password_hash
from app.models.users import User, UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup", response_model=UserPublic)
async def create_user(session: SessionDep, user_in: UserCreate):
    # Check if the email already exists
    statement = select(User).where(User.email == user_in.email)
    user = session.exec(statement).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    db_user = User.model_validate(
        user_in,
        update={"hashed_password": create_password_hash(user_in.password)},
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
