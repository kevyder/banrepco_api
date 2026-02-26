from datetime import datetime

from pydantic import BaseModel


class DatabaseHealthStatus(BaseModel):
    """Database connectivity status."""
    connected: bool
    error: str | None = None


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str  # "healthy" or "unhealthy"
    timestamp: datetime
    version: str
    database: DatabaseHealthStatus
