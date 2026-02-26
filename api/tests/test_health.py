from datetime import datetime

from fastapi.testclient import TestClient


def test_health_check_healthy(client: TestClient):
    """Test health check endpoint returns healthy status."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.1.0"
    assert "timestamp" in data
    assert "database" in data
    assert data["database"]["connected"] is True
    assert data["database"]["error"] is None


def test_health_check_response_structure(client: TestClient):
    """Test health check response has all required fields."""
    response = client.get("/health")
    data = response.json()

    # Verify all required fields are present
    required_fields = ["status", "timestamp", "version", "database"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Verify database object structure
    assert "connected" in data["database"]


def test_health_check_timestamp_is_valid(client: TestClient):
    """Test that timestamp is a valid ISO datetime."""
    response = client.get("/health")
    data = response.json()

    # This should not raise an exception
    timestamp = datetime.fromisoformat(data["timestamp"])
    assert isinstance(timestamp, datetime)


def test_health_check_version_matches(client: TestClient):
    """Test that version matches expected version."""
    response = client.get("/health")
    data = response.json()
    assert data["version"] == "0.1.0"
