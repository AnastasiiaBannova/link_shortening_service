from aiopg.sa import SAConnection
from sqlalchemy import delete, insert, select

from link_shortening_service.models.link import Link, LinkCreate
from link_shortening_service.repositories.postgres.errors import NotFoundError
from link_shortening_service.repositories.postgres.models.link import link


class LinkPostgresRepository:

    def __init__(self, connection: SAConnection):
        self._connection = connection
        self._table = link

    async def get_by_token(self, token: str) -> Link:
        query = select([self._table]).where(self._table.c.token == token).limit(1)
        rows = await self._connection.execute(query)
        row = await rows.first()
        if row is None:
            raise NotFoundError('Entity not found')
        return Link(**row)

    async def get_by_url(self, url: str) -> Link:
        query = select([self._table]).where(self._table.c.url == url).limit(1)
        rows = await self._connection.execute(query)
        row = await rows.first()
        if row is None:
            raise NotFoundError('Entity not found')
        return Link(**row)

    async def create(self, link: LinkCreate) -> int:
        statement = (
            insert(self._table).values(**link.dict()).returning(self._table.c.id)
        )
        return await self._connection.scalar(statement)  # type: ignore

    async def delete(self, token: str) -> None:
        statement = delete(self._table).where(self._table.c.token == token)
        cursor = await self._connection.execute(statement)
        if cursor.rowcount == 0:
            raise NotFoundError('Entity not found')
