# TODO: Test tasks for
# - Create a new tasks
# - Update tasks


from fastapi.testclient import TestClient

from app.core.config import settings


def test_create_new_task(client: TestClient, user_token_headers: dict[str, str]):
    response = client.post(
        f"{settings.API_V1_STR}/tasks/",
        headers=user_token_headers,
        json={"title": "Tasks management api test task"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Tasks management api test task"
