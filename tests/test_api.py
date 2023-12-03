from fastapi.testclient import TestClient
from pytest import mark


@mark.asyncio
async def test_get_tasks_without_date_parameter(client: TestClient):
    response = client.get("/tasks")
    assert response.status_code == 422


@mark.asyncio
async def test_get_tasks(today_date: str, client: TestClient):
    response = client.get("/tasks", params={"tasks_date": today_date})
    assert response.status_code == 200


@mark.asyncio
async def test_create_task(
    today_date: str,
    task_description: str,
    client: TestClient,
):
    response = client.post(
        "/tasks",
        json={
            "description": task_description,
            "tasksDate": today_date,
        },
    )
    assert response.status_code == 200


@mark.asyncio
async def test_status_update(
    today_date: str,
    task_description: str,
    client: TestClient,
):
    # Create task
    created_task_response = client.post(
        "tasks",
        json={
            "description": task_description,
            "tasksDate": today_date,
        }
    )
    assert created_task_response.status_code == 200
    created_task: dict = created_task_response.json()
    assert created_task.get("isCompleted") == False

    created_task_id = created_task.get("uuid") 

    # Set task as completed
    updated_task_status_response = client.patch(
        f"tasks/{created_task_id}/complete",
        json={"isCompleted": True}
    )
    assert updated_task_status_response.status_code == 200
    updated_task: dict = updated_task_status_response.json()
    assert updated_task.get("isCompleted") == True

    # Set the same task as uncompleted
    updated_again_task_status_response = client.patch(
        f"tasks/{created_task_id}/complete",
        json={"isCompleted": False}
    )
    assert updated_again_task_status_response.status_code == 200
    updated_once_again_task: dict = updated_again_task_status_response.json()
    assert updated_once_again_task.get("isCompleted") == False

    # Check the tested task in list of tasks
    all_todays_tasks_response = client.get(
        "/tasks", params={"tasks_date": today_date},
    )
    assert all_todays_tasks_response.status_code == 200
    todays_tasks: list[dict] = all_todays_tasks_response.json()

    found_task: dict | None = next(
        (task for task in todays_tasks if task.get("uuid") == created_task_id),
        None,
    )
    assert found_task is not None
    assert found_task.get("isCompleted") == False
