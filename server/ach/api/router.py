from fastapi import APIRouter

from server.ach.api.v1 import v1_router

ach_api_router = APIRouter()

ach_api_router.include_router(v1_router)
