from app.web.schemes import BaseModel


class HealthCheckResponse(BaseModel):
    is_healthy: bool
    timestamp: str
