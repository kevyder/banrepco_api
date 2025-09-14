import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_database_url() -> str:
    """Get the appropriate database URL."""

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL is required.")

    return f"sqlite+{database_url}?secure=true"


def get_connect_args() -> dict:
    """Get database connection arguments."""

    auth_token = os.environ.get("DATABASE_AUTH_TOKEN")
    if not auth_token:
        raise ValueError("DATABASE_AUTH_TOKEN is required.")

    return {"auth_token": auth_token}


def create_sync_engine():
    """Create a synchronous SQLAlchemy engine."""
    return create_engine(
        url=get_database_url(),
        connect_args=get_connect_args(),
    )


db_engine = create_sync_engine()
