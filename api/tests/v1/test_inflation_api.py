import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.inflation import Inflation


@pytest.fixture(scope="function")
def sample_inflation_data(db_session_test: Session):
    """Create sample inflation data for testing."""
    data = [
        Inflation(year=2023, month=1, inflation_rate=13.25, target=3.0),
        Inflation(year=2023, month=2, inflation_rate=13.28, target=3.0),
        Inflation(year=2023, month=3, inflation_rate=13.34, target=3.0),
        Inflation(year=2024, month=1, inflation_rate=9.25, target=3.0),
        Inflation(year=2024, month=2, inflation_rate=8.75, target=3.0),
    ]

    for item in data:
        db_session_test.add(item)

    db_session_test.commit()


def test_get_inflation_data(client: TestClient, sample_inflation_data):
    """Test getting paginated inflation data."""
    response = client.get("/v1/inflation")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data

    # Verify sorting (default desc)
    items = data["items"]
    assert items[0]["year"] >= items[-1]["year"]
    if items[0]["year"] == items[-1]["year"]:
        assert items[0]["month"] >= items[-1]["month"]


def test_get_inflation_data_sort_asc(client: TestClient, sample_inflation_data):
    """Test getting inflation data sorted in ascending order."""
    response = client.get("/v1/inflation?sort=asc")
    assert response.status_code == 200

    data = response.json()
    items = data["items"]
    assert items[0]["year"] <= items[-1]["year"]
    if items[0]["year"] == items[-1]["year"]:
        assert items[0]["month"] <= items[-1]["month"]


def test_get_inflation_by_date_range(client: TestClient, sample_inflation_data):
    """Test getting inflation data by date range."""
    params = {"start_year": 2023, "start_month": 1, "end_year": 2023, "end_month": 12}
    response = client.get("/v1/inflation/date-range", params=params)
    assert response.status_code == 200

    data = response.json()
    items = data["items"]
    assert len(items) == 3  # From sample data
    for item in items:
        assert item["year"] == 2023
        assert 1 <= item["month"] <= 12


def test_get_inflation_by_specific_date(client: TestClient, sample_inflation_data):
    """Test getting inflation data for a specific date."""
    response = client.get("/v1/inflation/2023/01")
    assert response.status_code == 200

    data = response.json()
    assert data["year"] == 2023
    assert data["month"] == 1
    assert data["inflation_rate"] == 13.25
    assert data["target"] == 3.0


def test_get_inflation_by_nonexistent_date(client: TestClient, sample_inflation_data):
    """Test getting inflation data for a date that doesn't exist."""
    response = client.get("/v1/inflation/2020/1")
    assert response.status_code == 404
    assert "No inflation data found" in response.json()["detail"]


def test_invalid_date_range(client: TestClient, sample_inflation_data):
    """Test invalid date range parameters."""
    # Invalid month
    params = {
        "start_year": 2023,
        "start_month": 13,  # Invalid month
        "end_year": 2023,
        "end_month": 12,
    }
    response = client.get("/v1/inflation/date-range", params=params)
    assert response.status_code == 422

    # Invalid year
    params = {
        "start_year": 1800,  # Invalid year
        "start_month": 1,
        "end_year": 2023,
        "end_month": 12,
    }
    response = client.get("/v1/inflation/date-range", params=params)
    assert response.status_code == 422
