from link_shortening_service.core.errors import BaseError


class NotFoundError(BaseError):
    message = 'Entity not found'
