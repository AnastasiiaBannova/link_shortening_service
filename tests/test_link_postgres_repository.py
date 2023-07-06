import pytest

from link_shortening_service.models.link import LinkCreate
from link_shortening_service.repositories.postgres.errors import NotFoundError


async def test_create(link_postgres_repository):
    link_id = await link_postgres_repository.create(
        LinkCreate(
            token='test_token',
            url='test_url'
        )
    )

    assert link_id


async def test_get_by_token(link_postgres_repository, link):
    get_link = await link_postgres_repository.get_by_token('test_token')
    assert get_link.id == link


async def test_get_by_token__not_found(link_postgres_repository):
    with pytest.raises(NotFoundError):
        await link_postgres_repository.get_by_token('test_token')


async def test_get_by_url(link_postgres_repository, link):
    get_link = await link_postgres_repository.get_by_url('test_url')
    assert get_link.id == link


async def test_get_by_url__not_found(link_postgres_repository):
    with pytest.raises(NotFoundError):
        await link_postgres_repository.get_by_url('test_url')


async def test_delete(link_postgres_repository, link):
    await link_postgres_repository.delete('test_token')


async def test_delete__not_found(link_postgres_repository):
    with pytest.raises(NotFoundError):
        await link_postgres_repository.delete('test_token')
