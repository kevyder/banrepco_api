import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from src.db.session import database_session
from src.main import app
from src.models.base import Base


@pytest.fixture(scope="function")
def db_session_test():
    database_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def client(db_session_test: Session) -> Generator[TestClient, None, None]:
    def override_get_db():
        return db_session_test
    app.dependency_overrides[database_session.get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
