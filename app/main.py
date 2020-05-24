from fastapi import FastAPI
from .routers import backtest, factorRegression, optimizeFactor

app = FastAPI()

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