import fastapi
from starlette.middleware.cors import CORSMiddleware

from link_shortening_service.api.api import router
from link_shortening_service.core.events import (create_start_app_handler,
                                                 create_stop_app_handler)
from link_shortening_service.core.settings import settings


def get_app() -> fastapi.FastAPI:
    app_ = fastapi.FastAPI(
        title=settings.MICROSERVICE_NAME,
        debug=settings.DEBUG,
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app_.add_event_handler("startup", create_start_app_handler(app_))
    app_.add_event_handler("shutdown", create_stop_app_handler(app_))

    app_.include_router(router)

    return app_


app = get_app()
