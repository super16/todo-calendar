from asyncio import get_event_loop_policy
from collections.abc import AsyncGenerator
from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from alembic.command import upgrade
from alembic.config import Config
from todo_calendar.application.config import Settings
from todo_calendar.application.database import get_async_session
from todo_calendar.main import app

TEST_CALENDAR_PATH = "test_calendar.db"

@fixture(scope="session")
def event_loop():
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
def testing_settings():
    return Settings(database_uri=f"sqlite+aiosqlite:///{TEST_CALENDAR_PATH}")


@fixture(scope="session")
def task_description():
    return "Test description"


@fixture(scope="session")
def today_date():
    today = date.today()
    return today.isoformat()


@fixture(scope="session")
async def get_test_async_session(
    testing_settings: Settings,
) -> AsyncGenerator[AsyncSession, None]:
    test_async_session = async_sessionmaker(
        bind=create_async_engine(url=testing_settings.database_uri),
        expire_on_commit=False,
    )
    async with test_async_session() as session:
        yield session


@fixture(scope="session")
async def client(
    testing_settings: Settings,
    get_test_async_session: AsyncSession
):
    test_engine = create_async_engine(testing_settings.database_uri)

    def run_upgrade(connection, alembic_config: Config):
        alembic_config.attributes["connection"] = connection
        upgrade(alembic_config, "head")

    async with test_engine.begin():
        test_alembic_config = Config("alembic.ini")
        test_alembic_config.set_main_option(
            "sqlalchemy.url",
            testing_settings.database_uri,
        )
        async with test_engine.begin() as conn:
            await conn.run_sync(run_upgrade, test_alembic_config)

    app.dependency_overrides[get_async_session] = \
        lambda: get_test_async_session

    yield TestClient(app)

    # Clear the database
    Path(TEST_CALENDAR_PATH).unlink()
