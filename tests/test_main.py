from fastapi.testclient import TestClient
import json

from app.main import app

client = TestClient(app)

# python -m pytest

with open('./test_data/backtest.json', 'r') as file:
    backtestInput = file.read()
backtestInput = json.loads(backtestInput)


def test_backtest():
    response = client.post("/backtest/", json=backtestInput)
    assert response.status_code == 200
    assert response.json()['backtest'][0] == {
        "date": "2019-03-13",
        "output": 10000.0,
        "drawdown_pct": 0.0,
        "benchmark": 10000.0
    }


with open('./test_data/factorRegression.json', 'r') as file:
    factorRegressionInput = file.read()
factorRegressionInput = json.loads(factorRegressionInput)


def test_factorRegression():
    response = client.post("/factorRegression/", json=factorRegressionInput)
    assert response.status_code == 200
    assert response.json() == {
        "nobs": 27.0,
        "rsquared": 0.10331289522729892,
        "rsquared_adj": -0.013646292351749079,
        "fvalue": 0.8833243233454736,
        "coeff": {
            "Intercept": -16.4577686646,
            "MktMinRF": -0.1752112494,
            "SMB": 0.2212859239,
            "HML": -0.298361303
        },
        "pvals": {
            "Intercept": 0.0,
            "MktMinRF": 31.3859217102,
            "SMB": 54.5978229272,
            "HML": 24.6858435783
        },
        "conf_lower": {
            "Intercept": -18.1341640453,
            "MktMinRF": -0.5272096868,
            "SMB": -0.525639616,
            "HML": -0.8177846272
        },
        "conf_higher": {
            "Intercept": -14.7813732838,
            "MktMinRF": 0.176787188,
            "SMB": 0.9682114638,
            "HML": 0.2210620211
        }
    }


with open('./test_data/optimization.json', 'r') as file:
    optimizeFactorInput = file.read()
optimizeFactorInput = json.loads(optimizeFactorInput)


def test_optimizeFactor():
    response = client.post("/optimizeFactor/", json=optimizeFactorInput)
    assert response.status_code == 200
    assert response.json() == [-0.12857146205000275,
                               0.6201521681595863, 0.5084192938904165]
