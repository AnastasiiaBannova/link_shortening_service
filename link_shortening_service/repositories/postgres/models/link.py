from sqlalchemy import Column, Integer, String, Table

from link_shortening_service.repositories.postgres.models.base import metadata

link = Table(
    'link',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('token', String, nullable=False),
    Column('url', String, nullable=False),
)
