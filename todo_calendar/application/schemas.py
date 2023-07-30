from datetime import date

from pydantic import BaseModel


class TaskBase(BaseModel):
    description: str


class TaskCreate(TaskBase):
    tasks_date: date | None = None


class TaskItem(TaskCreate):
    uuid: str
    is_completed: bool
    is_reoccurring: bool

