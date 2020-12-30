import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_fund_response_code():
    response = client.post(
        "/backtest/",
        json={
            "startDate": "2018-12-31",
            "endDate": "2019-01-31",
            "portfolio": [
                {"fund": "MMM", "amount": 1000},
            ],
            "strategy": {"rebalance": False, "rebalanceFrequency": "Y"},
        },
    )
    assert response.status_code == 200


def test_fund_response_backtest_rebalancefalse():
    response = client.post(
        "/backtest/",
        json={
            "startDate": "2018-12-31",
            "endDate": "2020-01-31",
            "portfolio": [
                {"fund": "MMM", "amount": 1000},
                {"fund": "ABT", "amount": 1000},
            ],
            "strategy": {"rebalance": False, "rebalanceFrequency": "Y"},
        },
    )
    assert response.json()['projection'][0] == {
        "MMM": 1000,
        "ABT": 1000,
        "portfolio": 2000,
        "date": "2018-12-31",
    }

    assert response.json()['projection'][-1] == {
        "MMM": 832.6860502,
        "ABT": 1204.7559795,
        "portfolio": 2037.4420297,
        "date": "2020-01-31",
    }


def test_fund_response_backtest_rebalancetrue():
    response = client.post(
        "/backtest/",
        json={
            "startDate": "2018-12-31",
            "endDate": "2020-01-31",
            "portfolio": [
                {"fund": "MMM", "amount": 1000},
                {"fund": "ABT", "amount": 1000},
            ],
            "strategy": {"rebalance": True, "rebalanceFrequency": "Y"},
        },
    )
    assert response.json()['projection'][0] == {
        "MMM": 1000,
        "ABT": 1000,
        "portfolio": 2000,
        "date": "2018-12-31",
    }

    assert response.json()['projection'][-1] == {
        "MMM": 979.5458631406,
        "ABT": 1091.5477455713,
        "portfolio": 2071.0936087119,
        "date": "2020-01-30",
    }


def test_fund_response_backtest_rebalancetrue():
    response = client.post(
        "/backtest/",
        json={
            "startDate": "2018-12-31",
            "endDate": "2020-01-31",
            "portfolio": [
                {"fund": "MMM", "amount": 1000},
                {"fund": "ABT", "amount": 1000},
            ],
            "strategy": {"rebalance": True, "rebalanceFrequency": "M"},
        },
    )
    assert response.json()['projection'][0] == {
        "MMM": 1000,
        "ABT": 1000,
        "portfolio": 2000,
        "date": "2018-12-31",
    }

    assert response.json()['projection'][-1] == {
        "MMM": 975.6435274948,
        "ABT": 1087.1992144438,
        "portfolio": 2062.8427419386,
        "date": "2020-01-30",
    }
