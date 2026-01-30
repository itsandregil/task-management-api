from sqlmodel import Session

from app import crud
from tests.utils import get_random_new_user


def test_create_new_user(db: Session):
    user_in = get_random_new_user()
    new_user = crud.create_user(session=db, user_create=user_in)
    assert new_user.email == user_in.email
    assert hasattr(new_user, "hashed_password")


def test_is_authenticated_user(db: Session):
    user_in = get_random_new_user()
    user = crud.create_user(session=db, user_create=user_in)
    authenticated_user = crud.authenticate(
        session=db,
        email=user_in.email,
        password=user_in.password,
    )

    assert authenticated_user is not None
    assert authenticated_user.email == user.email
    assert authenticated_user.hashed_password == user.hashed_password


def test_is_not_authenticated_user(db: Session):
    user_in = get_random_new_user()
    authenticated_user = crud.authenticate(
        session=db,
        email=user_in.email,
        password=user_in.password,
    )

    assert authenticated_user is None
