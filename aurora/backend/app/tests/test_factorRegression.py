import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_regression_response_code():
    response = client.post(
        "/factorRegression/",
        json={
            "startDate": "2017-12-31",
            "endDate": "2018-12-31",
            "funds": ["AAPL"],
            "regressionFactors": ["MktRF", "SMB", "HML"],
            "frequency": "monthly",
        },
    )
    assert response.status_code == 200


def test_apple_regression_12month():
    response = client.post(
        "/factorRegression/",
        json={
            "startDate": "2017-12-31",
            "endDate": "2019-12-31",
            "funds": ["AAPL"],
            "regressionFactors": ["MktRF", "SMB", "HML"],
            "frequency": "monthly",
        },
    )
    assert response.json()[0]["fundCode"] == "AAPL"
    assert response.json()[0]["numberObservations"] == 24
    assert response.json()[0]["rSquared"] == 0.3402966107590083
    assert response.json()[0]["fValue"] == 3.438884972740346
    assert response.json()[0]["coefficient"]["Intercept"] == 1.7044938638299891
    assert response.json()[0]["coefficient"]["MktRF"] == 105.19639234216007
    assert response.json()[0]["coefficient"]["SMB"] == 50.618061990173246
    assert response.json()[0]["coefficient"]["HML"] == -29.880837656903687
