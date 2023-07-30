from asyncio import get_event_loop_policy
from datetime import date
from pathlib import Path

from fastapi.testclient import TestClient
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import create_async_engine

from alembic.command import upgrade
from alembic.config import Config
from todo_calendar.application.config import Settings, get_settings
from todo_calendar.main import app


@fixture(scope="session")
def event_loop():
    policy = get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session")
def testing_settings():
    return Settings(database_uri="sqlite+aiosqlite:///test_calendar.db")


@fixture(scope="session")
def task_description() -> str:
    return "Test description"


@fixture(scope="session")
def today_date() -> str:
    today = date.today()
    return today.isoformat()


@fixture(scope="session")
async def client(testing_settings: Settings):
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

    app.dependency_overrides[get_settings] = lambda: testing_settings

    yield TestClient(app)

    Path("test_calendar.db").unlink(missing_ok=True)
