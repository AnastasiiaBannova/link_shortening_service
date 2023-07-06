from pydantic import BaseModel


class BaseLink(BaseModel):
    token: str
    url: str


class Link(BaseLink):
    id: int


class LinkCreate(BaseLink):
    ...
