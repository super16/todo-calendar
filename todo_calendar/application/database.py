from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from todo_calendar.application.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    pass


async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=create_async_engine(url=settings.database_uri, echo=settings.debug),
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
