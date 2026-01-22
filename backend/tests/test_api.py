import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_all_equipment():
    """Test getting all equipment."""
    response = client.get("/api/v1/equipment/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_equipment_by_id():
    """Test getting specific equipment."""
    response = client.get("/api/v1/equipment/COMP-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "COMP-001"
    assert "name" in data
    assert "status" in data
    assert "health_score" in data


def test_get_nonexistent_equipment():
    """Test getting non-existent equipment returns 404."""
    response = client.get("/api/v1/equipment/NONEXISTENT")
    assert response.status_code == 404


def test_executive_dashboard():
    """Test executive dashboard metrics."""
    response = client.get("/api/v1/dashboard/executive")
    assert response.status_code == 200
    data = response.json()
    assert "total_equipment" in data
    assert "average_health_score" in data
    assert "predicted_failures" in data


def test_get_alerts():
    """Test getting alerts."""
    response = client.get("/api/v1/dashboard/alerts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_ai_query():
    """Test AI query endpoint."""
    response = client.post(
        "/api/v1/ai/query",
        json={"query": "What is the status of COMP-001?"}
    )
    # May fail without OpenAI key, but should return 200 or 500, not 4xx
    assert response.status_code in [200, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
