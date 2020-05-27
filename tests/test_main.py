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
        "nobs": 4980.0,
        "rsquared": 0.0004338663695606648,
        "rsquared_adj": -0.00016876594573100867,
        "fvalue": 0.719952047959286,
        "coeff": {
            "Intercept": -0.0052637068,
            "MktMinRF": 0.0005944021,
            "SMB": 0.0020169948,
            "HML": -0.0019636165
        },
        "pvals": {
            "Intercept": 3.87348e-05,
            "MktMinRF": 0.5812138872,
            "SMB": 0.3610547771,
            "HML": 0.3142349127
        },
        "conf_lower": {
            "Intercept": -0.0077692088,
            "MktMinRF": -0.0015179753,
            "SMB": -0.0023119087,
            "HML": -0.0057883958
        },
        "conf_higher": {
            "Intercept": -0.0027582047,
            "MktMinRF": 0.0027067795,
            "SMB": 0.0063458983,
            "HML": 0.0018611628
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
