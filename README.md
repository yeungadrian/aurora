# Aurora
### Understanding financial markets

## Supported features:
- Historical backtesting of portfolio
- Over 500 US stocks

## Installation:
Run 
```html
docker-compose up --force-recreate --build -d
```
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive api docs

[http://127.0.0.1:8501](http://127.0.0.1:8501) for streamlit application

pytest
```html
pytest -p no:cacheprovider 
```

Stuff to add to github actions:
Removing pycache folders
find . -type d -name __pycache__ -exec rm -r {} \+
Black styling
black aurora
## Dependencies:
- Fastapi
- Streamlit
- Docker
