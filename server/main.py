import uvicorn
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from server.ach.api import ach_api_router
from server.core.api import core_api_router
from server.core.utils import sentry_io_service  # noqa
from server.dashboards.api import dashboard_api_router

api_prefix = "/api"

origins = [
    "http://localhost",
    "http://localhost:3000",
]
middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

# Init App

app = FastAPI(middleware=middlewares, openapi_url="/api/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")

app.include_router(dashboard_api_router, prefix=api_prefix, tags=["dashboard"])
app.include_router(core_api_router, prefix=api_prefix, tags=["core"])
app.include_router(ach_api_router, prefix=api_prefix, tags=["ach"])

from server.core.error_handlers import *  # noqa

# Entrypoint
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
