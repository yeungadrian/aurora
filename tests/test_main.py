from fastapi.testclient import TestClient
import json

from app.main import app

client = TestClient(app)

# python -m pytest

with open('./data/backtest.json', 'r') as file:
    backtestInput = file.read()
backtestInput = json.loads(backtestInput)


def test_backtest():
    response = client.post("/backtest/", json=backtestInput)
    assert response.status_code == 200
    assert response.json()['backtest'][0] == {
        "date": "2019-03-13",
        "output": 30988.5593824744,
        "drawdown_pct": 0.0,
        "benchmark": 10988.5593824744
    }

with open('./data/factorRegression.json', 'r') as file:
    factorRegressionInput = file.read()
factorRegressionInput = json.loads(factorRegressionInput)


def test_factorRegression():
    response = client.post("/factorRegression/", json=factorRegressionInput)
    assert response.status_code == 200
    assert response.json() == {
        "nobs": 252.0,
        "rsquared": 0.036129374187741536,
        "rsquared_adj": 0.028387441450293593,
        "fvalue": 4.666712488082352,
        "coeff": {
            "Intercept": 0.0021910735,
            "MktMinRF": -0.0035917798,
            "SMB": 0.0049139198
        },
        "pvals": {
            "Intercept": 0.25937604,
            "MktMinRF": 0.0071851308,
            "SMB": 0.1488124576
        },
        "conf_lower": {
            "Intercept": -0.0016263579,
            "MktMinRF": -0.0062016696,
            "SMB": -0.0017688497
        },
        "conf_higher": {
            "Intercept": 0.0060085048,
            "MktMinRF": -0.0009818901,
            "SMB": 0.0115966893
        }
    }

with open('./data/optimization.json', 'r') as file:
    optimizeFactorInput = file.read()
optimizeFactorInput = json.loads(optimizeFactorInput)

def test_optimizeFactor():
    response = client.post("/optimizeFactor/", json=optimizeFactorInput)
    assert response.status_code == 200
    assert response.json() == [-0.12857146205000275,0.6201521681595863,0.5084192938904165]


