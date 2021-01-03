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
                {"fund": "ABMD", "amount": 1000},
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
                {"fund": "ABMD", "amount": 1000},
                {"fund": "ATVI", "amount": 1000},
            ],
            "strategy": {"rebalance": False, "rebalanceFrequency": "Y"},
        },
    )
    assert response.json()["projection"][0] == {
        "portfolio": 2000,
        "drawdown": 0,
        "date": "2018-12-31",
    }

    assert response.json()["projection"][-1] == {
        "portfolio": 1828.8735022,
        "drawdown": -0.1428562454,
        "date": "2020-01-31",
    }


def test_fund_response_backtest_rebalancetrue():
    response = client.post(
        "/backtest/",
        json={
            "startDate": "2018-12-31",
            "endDate": "2020-01-31",
            "portfolio": [
                {"fund": "ABMD", "amount": 1000},
                {"fund": "ATVI", "amount": 1000},
            ],
            "strategy": {"rebalance": True, "rebalanceFrequency": "Y"},
        },
    )
    assert response.json()["projection"][0] == {
        "portfolio": 2000,
        "drawdown": 0,
        "date": "2018-12-31",
    }

    assert response.json()["projection"][-1] == {
        "portfolio": 1908.8516897582,
        "drawdown": -0.1053726229,
        "date": "2020-01-30",
    }


def test_fund_response_backtest_rebalancetrue():
    response = client.post(
        "/backtest/",
        json={
            "startDate": "2018-12-31",
            "endDate": "2020-01-31",
            "portfolio": [
                {"fund": "ABMD", "amount": 1000},
                {"fund": "ATVI", "amount": 1000},
            ],
            "strategy": {"rebalance": True, "rebalanceFrequency": "M"},
        },
    )
    assert response.json()["projection"][0] == {
        "portfolio": 2000,
        "drawdown": 0,
        "date": "2018-12-31",
    }

    assert response.json()["projection"][-1] == {
        "portfolio": 1810.4527720136,
        "drawdown": -0.1514895456,
        "date": "2020-01-30",
    }

    assert response.json()["metrics"]["cagr"] == -0.08795955335306682

    assert response.json()["metrics"]["monthly_std"] == 0.06859533681645001

    assert response.json()["metrics"]["downside_std"] == 0.028982315516618017

    assert response.json()["metrics"]["sharpe_ratio"] == -1.4280789030191758

    assert response.json()["metrics"]["sortino_ratio"] == -3.379976775730645

    assert response.json()["metrics"]["max_drawdown"] == -0.2761741096

    assert (
        response.json()["metrics"]["monthlyReturns"][0]["monthlyReturn"] == -0.045104214
    )
