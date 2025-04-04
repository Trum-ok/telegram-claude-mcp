from datetime import UTC, datetime

from fastapi import APIRouter

from app.health.schemes import HealthCheckResponse
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response

health_router = APIRouter()


@health_router.get(
        path="/health",
        response_model=OkResponseSchema[HealthCheckResponse],
        summary="Информация о состоянии сервиса",
        tags=["health"],
        )
async def health_check():
    data = {
        "is_healthy": True,
        "timestamp": datetime.now(UTC).strftime("%d/%m/%Y %H:%M:%S")
    }
    return json_response(data=data)
