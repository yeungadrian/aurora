import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fund_response_code():
    response = client.post(
        "/factorRegression/",
        json={
            "startDate": "2017-12-31",
            "endDate": "2018-03-31",
            "funds": ["AAPL"],
            "regressionFactors": ["MktRF", "SMB", "HML"],
        },
    )
    assert response.status_code == 200


def test_fund_response_backtest_rebalancefalse():
    response = client.post(
        "/factorRegression/",
        json={
            "startDate": "2017-12-31",
            "endDate": "2019-12-31",
            "funds": ["AAPL"],
            "regressionFactors": ["MktRF", "SMB", "HML"],
        },
    )
    assert response.json()[0]["fundCode"] == "AAPL"
    assert response.json()[0]["numberObservations"] == 503
    assert response.json()[0]["rSquared"] == 0.4783125383580532
    assert response.json()[0]["fValue"] == 152.50379725404886
    assert response.json()[0]["coefficient"]["Intercept"] == -0.7141998838464716
    assert response.json()[0]["coefficient"]["MktRF"] == 1.0345725482879313
    assert response.json()[0]["coefficient"]["SMB"] == -0.03265664268983073
    assert response.json()[0]["coefficient"]["HML"] == -0.335076299420108
