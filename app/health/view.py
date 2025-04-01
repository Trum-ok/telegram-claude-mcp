from datetime import UTC, datetime

from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat()
    }
