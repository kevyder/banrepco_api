from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.db.session import database_session
from src.schemas.health import DatabaseHealthStatus, HealthCheckResponse

router = APIRouter(tags=["health"])

# Application version - should match pyproject.toml
APP_VERSION = "0.1.0"


@router.get("/health", response_model=HealthCheckResponse, status_code=200)
async def health_check(
    db_session: Session = Depends(database_session.get_db),
) -> HealthCheckResponse:
    """
    Health check endpoint that verifies API and database connectivity.

    Returns:
        HealthCheckResponse: Status of the API and database with timestamp and version.
    """
    # Check database connectivity
    db_status = DatabaseHealthStatus(connected=True, error=None)
    overall_status = "healthy"

    try:
        # Execute a simple query to verify database connection
        db_session.execute(text("SELECT 1"))
    except Exception as e:
        db_status = DatabaseHealthStatus(connected=False, error=str(e))
        overall_status = "unhealthy"

    return HealthCheckResponse(
        status=overall_status,
        timestamp=datetime.now(timezone.utc),
        version=APP_VERSION,
        database=db_status,
    )
