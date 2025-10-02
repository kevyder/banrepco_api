from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.models.trm import TRM


@pytest.fixture(scope="function")
def sample_trm_data(db_session_test: Session):
    """Create sample TRM data for testing."""
    data = [
        TRM(date=date(2023, 1, 1), value=4850.50),
        TRM(date=date(2023, 1, 2), value=4855.75),
        TRM(date=date(2023, 1, 3), value=4860.25),
        TRM(date=date(2023, 2, 1), value=4900.00),
        TRM(date=date(2023, 2, 2), value=4910.50),
    ]

    for item in data:
        db_session_test.add(item)

    db_session_test.commit()


def test_get_trm_data(client: TestClient, sample_trm_data):
    """Test getting paginated TRM data."""
    response = client.get("/v1/trm")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data

    # Verify sorting (default desc)
    items = data["items"]
    assert len(items) > 0
    # Convert string dates to date objects for comparison
    dates = [date.fromisoformat(item["date"]) for item in items]
    assert dates[0] >= dates[-1]


def test_get_trm_data_sort_asc(client: TestClient, sample_trm_data):
    """Test getting TRM data sorted in ascending order."""
    response = client.get("/v1/trm?sort=asc")
    assert response.status_code == 200

    data = response.json()
    items = data["items"]
    assert len(items) > 0
    # Convert string dates to date objects for comparison
    dates = [date.fromisoformat(item["date"]) for item in items]
    assert dates[0] <= dates[-1]


def test_get_trm_by_date_range(client: TestClient, sample_trm_data):
    """Test getting TRM data by date range."""
    params = {
        "start_date": "2023-01-01",
        "end_date": "2023-01-31"
    }
    response = client.get("/v1/trm/by-date-range", params=params)
    assert response.status_code == 200

    data = response.json()
    items = data["items"]
    assert len(items) == 3  # From sample data
    for item in items:
        item_date = date.fromisoformat(item["date"])
        assert date(2023, 1, 1) <= item_date <= date(2023, 1, 31)


def test_get_trm_by_specific_date(client: TestClient, sample_trm_data):
    """Test getting TRM data for a specific date."""
    response = client.get("/v1/trm/by-date", params={"specific_date": "2023-01-01"})
    assert response.status_code == 200

    data = response.json()
    assert data["date"] == "2023-01-01"
    assert data["value"] == 4850.50


def test_get_trm_by_nonexistent_date(client: TestClient, sample_trm_data):
    """Test getting TRM data for a date that doesn't exist."""
    response = client.get("/v1/trm/by-date", params={"specific_date": "2020-01-01"})
    assert response.status_code == 404
    assert "No TRM data found" in response.json()["detail"]


def test_invalid_date_range(client: TestClient, sample_trm_data):
    """Test invalid date range parameters."""
    # End date before start date
    params = {
        "start_date": "2023-12-31",
        "end_date": "2023-01-01"
    }
    response = client.get("/v1/trm/by-date-range", params=params)
    assert response.status_code == 422

    # Invalid date format
    params = {
        "start_date": "2023-13-01",  # Invalid month
        "end_date": "2023-12-31"
    }
    response = client.get("/v1/trm/by-date-range", params=params)
    assert response.status_code == 422


def test_pagination(client: TestClient, sample_trm_data):
    """Test pagination of TRM data."""
    # Test with small page size
    response = client.get("/v1/trm?page=1&size=2")
    assert response.status_code == 200

    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5  # Total number of sample records
    assert data["page"] == 1
    assert data["size"] == 2

    # Test second page
    response = client.get("/v1/trm?page=2&size=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["page"] == 2


def test_empty_date_range(client: TestClient, sample_trm_data):
    """Test getting TRM data for a date range with no data."""
    params = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31"
    }
    response = client.get("/v1/trm/by-date-range", params=params)
    assert response.status_code == 200

    data = response.json()
    assert len(data["items"]) == 0
    assert data["total"] == 0
