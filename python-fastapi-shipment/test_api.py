"""Basic API tests using httpx."""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "SwiftRoute API is running"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

# TODO: Add tests for shipment endpoints
# TODO: Add tests for customer endpoints
