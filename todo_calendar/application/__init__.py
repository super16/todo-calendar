from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .tasks import tasks_router


def create_app() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse)
    app.include_router(tasks_router)
    return app
