from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.config import settings
from tests.utils import get_random_new_user


def test_get_access_token(db: Session, client: TestClient):
    new_user = get_random_new_user()
    crud.create_user(session=db, user_create=new_user)

    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": new_user.email, "password": new_user.password},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"


def test_get_access_token_with_incorrect_password(db: Session, client: TestClient):
    new_user = get_random_new_user()
    crud.create_user(session=db, user_create=new_user)

    response = client.post(
        f"{settings.API_V1_STR}/login/access-token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": new_user.email, "password": "incorrect"},
    )

    assert response.status_code == 401
