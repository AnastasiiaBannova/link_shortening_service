import pytest

from link_shortening_service.core.settings import settings
from link_shortening_service.repositories.postgres.errors import NotFoundError
from link_shortening_service.services.errors import InvalidShortURLError


async def test_get_or_create_short_url(link_shortening_service, link):
    short_url = await link_shortening_service.get_or_create_short_url('test_url')
    assert short_url

    assert short_url == settings.BASE_URL + 'test_token'


async def test_get_full_url(link_shortening_service, link):
    full_url = await link_shortening_service.get_full_url(settings.BASE_URL + 'test_token')

    assert full_url == 'test_url'


async def test_get_full_url__not_found(link_shortening_service):
    with pytest.raises(NotFoundError):
        await link_shortening_service.get_full_url(settings.BASE_URL + 'test_token')


async def test_get_full_url__invalid_url(link_shortening_service):
    with pytest.raises(InvalidShortURLError):
        await link_shortening_service.get_full_url('test_token')


async def test_delete_link(link_shortening_service, link):
    await link_shortening_service.delete_url(settings.BASE_URL + 'test_token')


async def test_delete_link__not_found(link_shortening_service):
    with pytest.raises(NotFoundError):
        await link_shortening_service.delete_url(settings.BASE_URL + 'test_token')


async def test_delete_link__invalid_url(link_shortening_service):
    with pytest.raises(InvalidShortURLError):
        await link_shortening_service.delete_url('test_token')
