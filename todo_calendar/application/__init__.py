from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles

from .tasks import tasks_router


def create_app() -> FastAPI:
    app = FastAPI(default_response_class=ORJSONResponse)
    app.include_router(tasks_router)
    app.mount(
        "/",
        StaticFiles(
            directory="todo_calendar/frontend/dist",
            html=True,
        ),
        name="static",
    )
    return app
