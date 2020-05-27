from fastapi import FastAPI
from .routers import backtest, factorRegression, optimizeFactor, stocks

app = FastAPI()

app.include_router(
    stocks.router,
    prefix="/stocks"
)

app.include_router(
    backtest.router,
    prefix="/backtest"
)

app.include_router(
    factorRegression.router,
    prefix="/factorRegression"
)

app.include_router(
    optimizeFactor.router,
    prefix="/optimizeFactor"
)