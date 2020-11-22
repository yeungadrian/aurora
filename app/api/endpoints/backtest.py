from fastapi import APIRouter

from app import schemas
from app.data.data_loader import loadHistoricalIndex
from app.calculations.backtestCalculator import backTestModel

router = APIRouter()


@router.post("/")
def backtest(item: schemas.backtest):
    portfolio = item.dict()["portfolio"]
    fund_codes = []
    for i in portfolio:
        fund_codes.append(i["fund"])
    historicalData = loadHistoricalIndex(
        fund_codes=fund_codes,
        start_date=item.dict()["startDate"],
        end_date=item.dict()["endDate"],
    )
    test = backTestModel(historical_index = historicalData, portfolio = portfolio, strategy = item.dict()["strategy"] )
    return test
