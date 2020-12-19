import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_response():
    response = client.get("/funds")
    assert response.status_code == 200