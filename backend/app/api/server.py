from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core import tasks
from app.core.config import settings
from app.api.routes import router as api_router


def get_application():
    app = FastAPI(title=settings.project_name, version=settings.version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))
    app.include_router(api_router, prefix=settings.api_prefix)

    return app


app = get_application()
