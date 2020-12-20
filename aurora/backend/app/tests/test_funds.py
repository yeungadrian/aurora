import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fund_response_code():
    response = client.get("/funds")
    assert response.status_code == 200


def test_fund_value():
    response = client.get("/funds")
    assert response.json()[0]["Code"] == "MMM"
    assert response.json()[0]["Company"] == "3M Company"


def test_fund_value():
    response = client.get("/funds")
    assert response.json()[5]["Code"] == "ATVI"
    assert response.json()[5]["Company"] == "Activision Blizzard"
