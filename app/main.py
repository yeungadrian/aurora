from fastapi import FastAPI
from .routers import backtest, factorRegression

app = FastAPI()

app.include_router(
    backtest.router,
    prefix="/backtest"
)

app.include_router(
    factorRegression.router,
    prefix="/factorRegression"
)