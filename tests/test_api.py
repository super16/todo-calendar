from fastapi.testclient import TestClient
from pytest import mark


@mark.asyncio
async def test_get_tasks_without_date_parameter(client: TestClient):
    response = client.get("/tasks/")
    assert response.status_code == 422


@mark.asyncio
async def test_get_tasks(today_date: str, client: TestClient):
    response = client.get("/tasks/", params={"tasks_date": today_date})
    assert response.status_code == 200


@mark.asyncio
async def test_create_task(
    today_date: str,
    task_description: str,
    client: TestClient,
):
    response = client.post(
        "/tasks/",
        json={
            "description": task_description,
            "tasks_date": today_date,
        },
    )
    assert response.status_code == 200
