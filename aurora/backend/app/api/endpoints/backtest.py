from fastapi import APIRouter

from app import schemas
from app.data.dataLoader import load_historical_index
from app.calculations.backtestCalculator import backtest_strategy

router = APIRouter()


@router.post("/")
def backtest(item: schemas.backtest):
    portfolio = item.dict()["portfolio"]
    fund_codes = []
    for i in portfolio:
        fund_codes.append(i["fund"])
    historicalData = load_historical_index(
        fund_codes=fund_codes,
        start_date=item.dict()["startDate"],
        end_date=item.dict()["endDate"],
    )
    result = backtest_strategy(
        historical_index=historicalData,
        portfolio=portfolio,
        strategy=item.dict()["strategy"],
        start_date=item.dict()["startDate"],
        end_date=item.dict()["endDate"],
    )
    return result
