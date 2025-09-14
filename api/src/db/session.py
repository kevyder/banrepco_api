from typing import Generator

from sqlalchemy.orm import Session, sessionmaker

from src.db.db_engine import db_engine


class DatabaseSession:
    """Database session manager."""

    def __init__(self):
        """Initialize the session maker with the engine."""
        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db_engine,
        )

    def get_db(self) -> Generator[Session, None, None]:
        """Get a database session.

        Yields:
            Session: A SQLAlchemy session instance.

        Note:
            This method is designed to be used as a dependency in FastAPI.
            It ensures the session is properly closed after use.
        """
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()


# Create a single instance to be used throughout the application
db = DatabaseSession()
