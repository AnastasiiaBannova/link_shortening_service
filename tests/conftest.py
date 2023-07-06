import aiopg
import pytest
from httpx import AsyncClient

from alembic import command
from alembic.config import Config
from link_shortening_service.api.dependencies import _get_engine
from link_shortening_service.core.settings import settings
from link_shortening_service.main import app

from .fixture import *  # noqa: F401 F403; because of fixture dir nested structure


@pytest.fixture
def application(engine):
    app.dependency_overrides[_get_engine] = lambda: engine

    yield app

    app.dependency_overrides = {}


@pytest.fixture
async def client(application):
    async with AsyncClient(app=application, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def engine(event_loop):
    engine = await aiopg.sa.create_engine(
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )

    alembic_cfg = Config('alembic.ini')
    command.downgrade(alembic_cfg, 'base')
    command.upgrade(alembic_cfg, 'head')

    yield engine

    command.downgrade(alembic_cfg, 'base')

    engine.close()
    await engine.wait_closed()


@pytest.fixture
async def conn(engine: aiopg.sa.Engine):
    async with engine.acquire() as conn:
        yield conn
