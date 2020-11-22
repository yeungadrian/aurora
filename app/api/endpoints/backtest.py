from fastapi import APIRouter

from app import schemas
from app.data.data_loader import loadHistoricalReturns

router = APIRouter()


@router.post("/")
def backtest(item: schemas.backtest):
    portfolio = item.dict()["portfolio"]
    fund_codes = []
    for i in portfolio:
        fund_codes.append(i["fund"])
    historicalData = loadHistoricalReturns(
        fund_codes=fund_codes,
        start_date=item.dict()["startDate"],
        end_date=item.dict()["endDate"],
    )
    return historicalData
