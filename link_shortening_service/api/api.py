from fastapi import APIRouter, Depends, HTTPException

from link_shortening_service.api.dependencies import \
    get_link_shortening_service
from link_shortening_service.api.schemas import URLSchema
from link_shortening_service.repositories.postgres.errors import NotFoundError
from link_shortening_service.services.errors import InvalidShortURLError
from link_shortening_service.services.link_shortening_service import \
    LinkShorteningService

router = APIRouter()


@router.post(path='/create_short_url', response_model=URLSchema, summary='Get or create short url')
async def create_short_url(
    full_url: URLSchema,
    link_shortening_service: LinkShorteningService = Depends(get_link_shortening_service),
) -> URLSchema:
    return URLSchema(url=await link_shortening_service.get_or_create_short_url(full_url.url))


@router.post(path='/get_full_url', response_model=URLSchema)
async def get_full_url(
    short_url: URLSchema,
    link_shortening_service: LinkShorteningService = Depends(get_link_shortening_service)
) -> URLSchema:
    try:
        return URLSchema(url=await link_shortening_service.get_full_url(short_url.url))
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail="Link not found") from exc
    except InvalidShortURLError as exc:
        raise HTTPException(status_code=400, detail="Invalid short url") from exc


@router.delete(path='/delete_url')
async def delete_url(
    short_url: URLSchema,
    link_shortening_service: LinkShorteningService = Depends(get_link_shortening_service)
) -> None:
    try:
        return await link_shortening_service.delete_url(short_url.url)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail="Link not found") from exc
    except InvalidShortURLError as exc:
        raise HTTPException(status_code=400, detail="Invalid short url") from exc
