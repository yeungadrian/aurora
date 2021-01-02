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
    assert response.json()["projection"][0] == {
        "portfolio": 2000,
        "drawdown": 0,
        "date": "2018-12-31",
    }

    assert response.json()["projection"][-1] == {
        "portfolio": 2037.4420297,
        "drawdown": -0.083364665,
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
    assert response.json()["projection"][0] == {
        "portfolio": 2000,
        "drawdown": 0,
        "date": "2018-12-31",
    }

    assert response.json()["projection"][-1] == {
        "portfolio": 2071.0936087119,
        "drawdown": -0.068224982,
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
    assert response.json()["projection"][0] == {
        "portfolio": 2000,
        "drawdown": 0,
        "date": "2018-12-31",
    }

    assert response.json()["projection"][-1] == {
        "portfolio": 2062.8427419386,
        "drawdown": -0.0722154685,
        "date": "2020-01-30",
    }

    assert response.json()["metrics"]["cagr"] == 0.029020825895222035

    assert response.json()["metrics"]["monthly_std"] == 0.05116237684014537

    assert response.json()["metrics"]["downside_std"] == 0.025292014385294763

    assert response.json()["metrics"]["sharpe_ratio"] == 0.37177369524195053

    assert response.json()["metrics"]["sortino_ratio"] == 0.7520486745524345

    assert response.json()["metrics"]["max_drawdown"] == -0.162734895

    assert response.json()["metrics"]["monthlyReturns"][0]["monthlyReturn"] == -0.0292249073
