from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from app.models.users import User, UserCreate

faker = Faker()


def get_random_new_user() -> UserCreate:
    """Returns required data to create a new user."""
    new_user = UserCreate(
        full_name=faker.name(),
        email=faker.email(),
        password=faker.password(),
    )
    return new_user


def get_access_token_headers(
    *, db: Session, client: TestClient
) -> dict[str, str | User]:
    user_data = get_random_new_user()
    _ = crud.create_user(session=db, user_create=user_data)

    login_data = {"username": user_data.email, "password": user_data.password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    data = r.json()

    return {"Authorization": f"Bearer {data['access_token']}"}
