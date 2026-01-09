from sqlmodel import Session, select

from app.core.security import create_password_hash, verify_password_hash
from app.models.users import User, UserCreate


def get_user_by_email(*, session: Session, email: str) -> User | None:
    """Finds first user with a given email"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    """Authenticate if the user exists and credentials are valid"""
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None
    if not verify_password_hash(password, user.hashed_password):
        return None
    return user


def create_user(*, session: Session, user_create: UserCreate):
    """Create a new user in the database with a hashed password"""
    new_user = User.model_validate(
        user_create,
        update={"hashed_password": create_password_hash(user_create.password)},
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
