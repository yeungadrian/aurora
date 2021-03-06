from fastapi import APIRouter

from app.api.endpoints import backtest
from app.api.endpoints import funds
from app.api.endpoints import factorRegression
from app.api.endpoints import frontier

api_router = APIRouter()

api_router.include_router(backtest.router, prefix="/backtest")
api_router.include_router(funds.router, prefix="/funds")
api_router.include_router(factorRegression.router, prefix="/factorRegression")
api_router.include_router(frontier.router, prefix="/portfolioOptimisation")
