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
Go to:

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

## Architecture:
- Goals:
1. Build out financial models to improve knowledge
2. Use financial models on real life data with interactive application

- Fastapi backend
    - Data is stored as parquet files (compressed files)
    - Avoiding databases for now as the focus is on building models
    - Standard fastapi code structure based loosely on https://fastapi.tiangolo.com/project-generation/
- Streamlit front end
    - Financial analysis requires visualisation, very difficult to get intuitive sense without visualisations and so command line gui's are ruled out
    - Do not want to learn javascript at the moment and so restricted to python libraries such as streamlit, dash
    - Streamlit looks to be the best to prototype something as fast as possible
- Data
    - Calling api's directly is too slow, especially when doing analysis of many funds, when using free tiers anyway
        - Used alphavantage to get a data dump of around 500 stocks and tidied it up into parquet files
## To Do:
- Roadmap of functionality:
    - Drawdowns to portfolio backtesting
    - Tidy up routes of backend
- Data:
    - Support funds and more stocks
    - Build makeshift ETL process to get data frequently
- Deployments:
  - How to deploy this to a cloud provider?
- CI:
    - Black Styling (black aurora)
    - Remove any pycache folders (find . -type d -name __pycache__ -exec rm -r {} \+) 
  
