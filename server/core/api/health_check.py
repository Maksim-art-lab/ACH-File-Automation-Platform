from fastapi import APIRouter

from server.core.schemas.base import StatusSchema
from server.core.status_enum import StatusEnum

router = APIRouter()


@router.get("/health-check/", response_model=StatusSchema)
async def get_health_check_status():
    """Get health check status"""
    return {"status": StatusEnum.success.value}
