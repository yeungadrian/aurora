# Aurora
### Understanding financial markets?

## Supported features:
- Historical backtesting of portfolios:
    - Over 500 US stocks supported
    - Rebalancing strategies
    - Metrics such as:
         - Compound annual growth rate
         - Sharpe ratio
         - Sortino ratio

## Installation:
Quick and easy local deployments using docker-compose, simply run:
```html
docker-compose up --force-recreate --build -d
```
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive api docs

[http://127.0.0.1:8501](http://127.0.0.1:8501) for streamlit application

Automated testing of backend using pytest, run locally by 
```html
cd aurora/backend
pytest -p no:cacheprovider aurora/backend
```

## Continous integration
Github Actions: https://github.com/yeungadrian/aurora/actions

## Major Dependencies:
- Fastapi
- Streamlit
- Docker
- Other dependencies in aurora/backend/requirements.txt and aurora/frontend/requirements.txt

## To Do:
- CI:
    - Black Styling (black aurora)
    - Remove any pycache folders (find . -type d -name __pycache__ -exec rm -r {} \+) 
- Data:
    - Support funds and more stocks
- Deployments:
  - How to deploy this to a cloud provider?
  
