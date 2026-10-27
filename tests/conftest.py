import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.main import app
from app.database import get_session
from app.models import Base, Link
from app.config import settings


# Test engine fixture
@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def test_engine():
    test_engine = create_async_engine(settings.db.test_url)

    yield test_engine

    await test_engine.dispose()


# Create and drop tables fixture
@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def prepare_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Override get session fixture
@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def db_session(test_engine, prepare_database):
    session_factory = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session


# Client fixture
@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://localhost:8000",
    ) as c:
        yield c

    app.dependency_overrides.clear()