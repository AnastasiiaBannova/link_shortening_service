import random
import string

from link_shortening_service.core.settings import settings
from link_shortening_service.models.link import LinkCreate
from link_shortening_service.repositories.postgres.errors import NotFoundError
from link_shortening_service.repositories.postgres.link import \
    LinkPostgresRepository
from link_shortening_service.services.errors import InvalidShortURLError


class LinkShorteningService:

    def __init__(
        self,
        link_postgres_repository: LinkPostgresRepository,
    ) -> None:
        self.link_postgres_repository = link_postgres_repository

    def _generate_token(self) -> str:
        char_set = string.ascii_uppercase + string.digits
        return ''.join(random.sample(char_set * 6, 6))

    def _get_token(self, short_url: str) -> str:
        if short_url.find(settings.BASE_URL) == -1:
            raise InvalidShortURLError('Invalid URL')
        return short_url.replace(settings.BASE_URL, '')

    async def get_or_create_short_url(self, full_url: str) -> str:
        try:
            link = await self.link_postgres_repository.get_by_url(full_url)
            token = link.token
        except NotFoundError:
            token = self._generate_token()
            await self.link_postgres_repository.create(
                LinkCreate(
                    token=token,
                    url=full_url,
                )
            )
        finally:
            return settings.BASE_URL + token

    async def get_full_url(self, short_url: str) -> str:
        token = self._get_token(short_url)
        link = await self.link_postgres_repository.get_by_token(token)
        return link.url

    async def delete_url(self, short_url: str) -> None:
        token = self._get_token(short_url)
        await self.link_postgres_repository.delete(token)
