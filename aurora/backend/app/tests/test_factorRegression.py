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
    assert response.json() == [
        {
            "fundCode": "AAPL",
            "numberObservations": 503,
            "rSquared": 0.478313,
            "rSquaredAdjusted": 0.475176,
            "fValue": 152.503797,
            "coefficient": [-0.7142, 1.034573, -0.032657, -0.335076],
            "pValues": [0, 0, 74.103074, 0.014619],
            "confidenceIntervalLower": [-0.812118, 0.929815, -0.22669, -0.5071],
            "confidenceIntervalHigher": [-0.616282, 1.139331, 0.161377, -0.163053],
        }
    ]
