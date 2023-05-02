import contextlib
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# Adapted from this tutorial:
# https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

Base = declarative_base()


class DatabaseSessionManager:
    """Utility object to manage our DB connection."""

    def __init__(self):
        """Set properties on the class to None."""
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    def is_initialized(self):
        """Determine if we have an engine."""
        return sessionmanager._engine is None

    def init(self, host: str):
        """Create real values for properties."""
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        """Close the current db session."""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Connect to the DB."""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Create a new session. Rolls back on uncaught exception."""
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        """Create all tables necessary, for tests."""
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        """Bobby Tables pays you a visit."""
        await connection.run_sync(Base.metadata.drop_all)


sessionmanager = DatabaseSessionManager()


async def get_db():
    """Get a DB session."""
    async with sessionmanager.session() as session:
        yield session
