# Aurora
### Understanding financial markets?

## Supported features:
- Historical backtesting of portfolios:
    - Rebalancing strategies
    - Metrics such as:
         - Compound annual growth rate
         - Sharpe ratio
         - Sortino ratio
         - Max drawdown

## Portfolio Backtesting
![](images/portfolioBacktest.png)

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
pytest -p no:cacheprovider 
```

## Major Dependencies:
- Fastapi
- Streamlit
- Docker
- Other dependencies in aurora/backend/requirements.txt and aurora/frontend/requirements.txt

## Continous integration
Github Actions: https://github.com/yeungadrian/aurora/actions
- Lint: Black https://github.com/psf/black#github-actions
- Integration tests using pytest: https://fastapi.tiangolo.com/tutorial/testing/

## Architecture:
- Goals:
1. Build out financial models to improve knowledge
2. Use financial models on real life data with interactive application

- Fastapi backend
    - Data is stored as parquet files (compressed files)
    - Avoiding databases for now as the focus is on building models
    - Standard fastapi code structure based loosely on https://fastapi.tiangolo.com/project-generation/
    - Only integration tests: cover all endpoints, allows to see if refactoring has changed calculations accidently
- Streamlit front end
    - Financial analysis requires visualisation, very difficult to get intuitive sense without visualisations and so command line gui's are ruled out
    - Do not want to learn javascript at the moment and so restricted to python libraries such as streamlit, dash
    - Streamlit looks to be the best to prototype something as fast as possible
    - Not worth investing in automated tests here yet
- Data
    - Calling api's directly is too slow, especially when doing analysis of many funds, when using free tiers anyway
    - Need to look for data sources and save as parquet files
    - Free API's are either too slow or have limits, which will be breached just deploying the app and testing changes
    
## Roadmap of functionality:
    - [ ] Tidy up routes of backend
    - [ ] Add images of app to readme
    - [ ] Factor Regression: French Fama
    - [ ] ETL process to get up to date data
    - [ ] Free data providers
    - [ ] Deployment to a cloud provider
