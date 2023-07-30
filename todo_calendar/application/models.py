from datetime import date, datetime

from sqlalchemy.dialects.sqlite import BOOLEAN, DATE, DATETIME, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import false
from sqlalchemy.sql.functions import current_timestamp

from .database import Base


class Task(Base):

    __tablename__ = "tasks"

    uuid: Mapped[str] = mapped_column(
        VARCHAR(),
        index=True,
        nullable=False,
        primary_key=True,
        sqlite_on_conflict_not_null="FAIL",
    )
    description: Mapped[str] = mapped_column(
        VARCHAR(256),
        nullable=False,
        sqlite_on_conflict_not_null="FAIL",
    )
    is_completed: Mapped[bool] = mapped_column(
        BOOLEAN(),
        nullable=False,
        server_default=false(),
        sqlite_on_conflict_not_null="FAIL",
    )
    is_reoccurring: Mapped[bool] = mapped_column(
        BOOLEAN(),
        nullable=False,
        server_default=false(),
        sqlite_on_conflict_not_null="FAIL",
    )
    tasks_date: Mapped[date] = mapped_column(
        DATE(),
        index=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DATETIME(),
        nullable=False,
        server_default=current_timestamp(),
        sqlite_on_conflict_not_null="FAIL",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DATETIME(),
        nullable=True,
    )
