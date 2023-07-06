from link_shortening_service.core.errors import BaseError


class InvalidShortURLError(BaseError):
    message = 'Invalid short url'
