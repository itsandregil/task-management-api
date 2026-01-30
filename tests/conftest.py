from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.main import SQLModel
from sqlmodel.pool import StaticPool

from app.api.deps import get_session
from app.main import app
from tests import utils


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    app.dependency_overrides[get_session] = lambda: db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def user_token_headers(db: Session, client: TestClient) -> dict[str, str]:
    return utils.get_access_token_headers(db=db, client=client)
