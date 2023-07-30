"""Init database

Revision ID: c260ab8804a7
Revises:
Create Date: 2023-07-16 19:50:11.102199

"""
from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.sqlite import BOOLEAN, DATE, DATETIME, VARCHAR
from sqlalchemy.sql import false
from sqlalchemy.sql.functions import current_timestamp

from alembic.op import create_index, create_table, drop_index, drop_table, f

revision = "c260ab8804a7"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    create_table("tasks",
        Column(
            "uuid",
            VARCHAR(),
            nullable=False,
            sqlite_on_conflict_not_null="FAIL",
        ),
        Column(
            "description",
            VARCHAR(length=256),
            nullable=False,
            sqlite_on_conflict_not_null="FAIL",
        ),
        Column(
            "is_completed",
            BOOLEAN(),
            server_default=false(),
            nullable=False,
            sqlite_on_conflict_not_null="FAIL",
        ),
        Column(
            "is_reoccurring",
            BOOLEAN(),
            server_default=false(),
            nullable=False,
            sqlite_on_conflict_not_null="FAIL",
        ),
        Column(
            "tasks_date",
            DATE(),
            nullable=True,
        ),
        Column(
            "created_at",
            DATETIME(),
            server_default=current_timestamp(),
            nullable=False,
            sqlite_on_conflict_not_null="FAIL",
        ),
        Column(
            "updated_at",
            DATETIME(),
            nullable=True,
        ),
        PrimaryKeyConstraint("uuid"),
    )
    create_index(
        f("ix_tasks_tasks_date"),
        "tasks",
        ["tasks_date"],
        unique=False,
    )
    create_index(f("ix_tasks_uuid"), "tasks", ["uuid"], unique=False)


def downgrade() -> None:
    drop_index(f("ix_tasks_uuid"), table_name="tasks")
    drop_index(f("ix_tasks_tasks_date"), table_name="tasks")
    drop_table("tasks")
