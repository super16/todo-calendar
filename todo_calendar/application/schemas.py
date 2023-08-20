from datetime import date

from pydantic import BaseModel, ConfigDict

from .utils import to_lower_camel


class TaskBase(BaseModel):
    description: str


class TaskCreate(TaskBase):
    model_config = ConfigDict(
        alias_generator=to_lower_camel,
        populate_by_name=True,
    )

    tasks_date: date | None = None


class TaskItem(TaskCreate):
    uuid: str
    is_completed: bool
    is_reoccurring: bool

