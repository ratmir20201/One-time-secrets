from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase

from config import settings
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

DATABASE_URL = settings.db.db_url
engine = create_async_engine(DATABASE_URL, echo=settings.db.echo)


_Session = async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    """Базовый класс для таблиц."""


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция для получения сессии."""
    async with _Session() as async_session:
        yield async_session
        await async_session.close()


@asynccontextmanager
async def get_async_context_session() -> AsyncGenerator[AsyncSession, None]:
    """Функция для получения сессии используя ее в контекстном менеджере."""
    async with _Session() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()