from typing import AsyncGenerator

from aiopg.sa import Engine, SAConnection
from fastapi import Depends, Request

from link_shortening_service.repositories.postgres.link import \
    LinkPostgresRepository
from link_shortening_service.services.link_shortening_service import \
    LinkShorteningService


def _get_engine(request: Request) -> Engine:
    return request.app.state.db_engine  # type: ignore


async def _get_connection(engine: Engine = Depends(_get_engine)) -> AsyncGenerator[SAConnection, None]:
    async with engine.acquire() as conn:
        yield conn


async def get_link_postgres_repository(
    connection: SAConnection = Depends(_get_connection)
) -> LinkPostgresRepository:
    return LinkPostgresRepository(connection)


async def get_link_shortening_service(
    link_postgres_repository: LinkPostgresRepository = Depends(get_link_postgres_repository)
) -> LinkShorteningService:
    return LinkShorteningService(link_postgres_repository)
