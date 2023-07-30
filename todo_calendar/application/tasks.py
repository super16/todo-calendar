from datetime import date
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import Task
from .schemas import TaskCreate, TaskItem

tasks_router = APIRouter(prefix="/tasks")


@tasks_router.get("/", response_model=list[TaskItem])
async def get_tasks(
    tasks_date: date,
    db_session: AsyncSession = Depends(get_async_session),  # noqa: B008
) -> list[TaskItem]:
    async with db_session.begin():
        result = await db_session.execute(
            select(Task).where(Task.tasks_date == tasks_date),
        )
        tasks = result.scalars()
    return [
        TaskItem.model_validate(task, from_attributes=True) for task in tasks
    ]


@tasks_router.post("/", response_model=TaskItem)
async def create_task(
    task: TaskCreate,
    db_session: AsyncSession = Depends(get_async_session),  # noqa: B008
) -> TaskItem:
    async with db_session.begin():
        unique_id = uuid4().hex
        result = await db_session.execute(
            insert(Task).values(
                uuid=unique_id,
                description=task.description,
                tasks_date=task.tasks_date,
            ).returning(Task),
        )
        created_task = result.scalar()
    return TaskItem.model_validate(
        created_task,
        from_attributes=True,
    )
