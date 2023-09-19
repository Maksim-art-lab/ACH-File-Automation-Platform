from fastapi import APIRouter

from server.core.api.health_check import router as health_check_router

core_api_router = APIRouter()

core_api_router.include_router(health_check_router)
