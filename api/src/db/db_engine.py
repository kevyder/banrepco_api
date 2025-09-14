import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.config.enums import Environment

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()


def get_database_url() -> str:
    """Get the appropriate database URL based on environment."""

    if ENVIRONMENT == Environment.DEVELOPMENT.value:
        return os.environ.get("DATABASE_URL", "sqlite+libsql:///local.db")

    # Production/Staging environment with Turso
    turso_url = os.environ.get("TURSO_DATABASE_URL")
    if not turso_url:
        raise ValueError("TURSO_DATABASE_URL is required for production environment")

    return f"sqlite+{turso_url}?secure=true"


def get_connect_args() -> dict:
    """Get connection arguments based on environment."""

    if ENVIRONMENT == Environment.DEVELOPMENT.value:
        return {}

    # Production/Staging environment with Turso auth token
    auth_token = os.environ.get("TURSO_AUTH_TOKEN")
    if not auth_token:
        raise ValueError("TURSO_AUTH_TOKEN is required for production environment")

    return {"auth_token": auth_token}


def create_sync_engine():
    """Create a synchronous SQLAlchemy engine."""
    return create_engine(
        url=get_database_url(),
        connect_args=get_connect_args(),
    )


db_engine = create_sync_engine()
