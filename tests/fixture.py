import pytest

from link_shortening_service.models.link import LinkCreate
from link_shortening_service.repositories.postgres.link import \
    LinkPostgresRepository
from link_shortening_service.services.link_shortening_service import \
    LinkShorteningService


@pytest.fixture
def link_postgres_repository(conn):
    return LinkPostgresRepository(conn)


@pytest.fixture
async def link(link_postgres_repository):
    return await link_postgres_repository.create(
        LinkCreate(
            token='test_token',
            url='test_url'
        )
    )


@pytest.fixture
def link_shortening_service(link_postgres_repository):
    return LinkShorteningService(link_postgres_repository)
