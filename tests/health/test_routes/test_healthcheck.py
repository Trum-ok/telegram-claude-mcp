from datetime import UTC, datetime

from fastapi.responses import Response
from httpx import AsyncClient


class TestHealthCheck:
    async def test_healthy(
        self, cli: AsyncClient
    ) -> None:
        response: Response = await cli.get('/health')
        assert response.status_code == 200

        data = response.json()
        assert data == {
            "status": "ok",
            "data": {
                "is_healthy": True,
                "timestamp": datetime.now(UTC).strftime("%d/%m/%Y %H:%M:%S"),
            },
        }
