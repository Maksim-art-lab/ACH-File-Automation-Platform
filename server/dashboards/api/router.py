from fastapi import APIRouter

from server.dashboards.api.v1 import v1_router

dashboard_api_router = APIRouter()

dashboard_api_router.include_router(v1_router)
