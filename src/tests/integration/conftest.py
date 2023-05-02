import asyncio
from contextlib import ExitStack

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main.database import get_db, sessionmanager
from main.main import init_app
from pytest_postgresql import factories
from pytest_postgresql.executor import PostgreSQLExecutor
from pytest_postgresql.janitor import DatabaseJanitor
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette.requests import Request


@pytest.fixture(autouse=True)
def app():
    """Get an instance of our app."""
    with ExitStack():
        yield init_app()


@pytest.fixture
def client(app: FastAPI):
    """Get a TestClient for our app."""
    with TestClient(app) as c:
        yield c


# Our library isn't as strongly typed as our linter.
test_db = factories.postgresql_proc(port=None, dbname="test_db")  # type: ignore


@pytest.fixture(scope="session")
def event_loop(request: Request):
    """Create a new session-scoped event loop fixture."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def connection_test(
    test_db: PostgreSQLExecutor, event_loop: asyncio.AbstractEventLoop
):
    """Replace connections in tests."""
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test: AsyncConnection):
    """Recreate the database tables."""
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app: FastAPI, connection_test: AsyncConnection):
    """Replace the session generator."""

    async def get_db_override():
        async with sessionmanager.session() as session:
            print("GetDB!")
            yield session

    app.dependency_overrides[get_db] = get_db_override
