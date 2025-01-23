import contextlib
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from settings.settings import get_settings

settings = get_settings()


Base = declarative_base()


ASYNC_DATABASE_URL = f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}/{settings.postgres_database}"


class DatabaseExceptionError(Exception):
    pass


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] | None = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine, expire_on_commit=False
        )

    async def is_initialised(self):
        return self._engine is not None

    async def close(self):
        if self._engine is None:
            raise DatabaseExceptionError("DatabaseSessionManager is not initialised")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise DatabaseExceptionError("DatabaseSessionManager is not initialised")
        async with self._engine.begin() as conn:
            try:
                yield conn
            except Exception as e:
                await conn.rollback()
                raise DatabaseExceptionError(
                    "Error with engine connection to database"
                ) from e

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise DatabaseExceptionError("DatabaseSessionManager is not initialised")
        session = self._sessionmaker()
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    ASYNC_DATABASE_URL, {"echo": settings.echo_database, "future": True}
)


async def get_async_db_session() -> AsyncSession:  # pyright: ignore [reportInvalidTypeForm]
    async with sessionmanager.session() as session:
        yield session  # pyright: ignore [reportReturnType]
