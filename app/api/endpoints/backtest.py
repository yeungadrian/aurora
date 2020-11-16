from fastapi import APIRouter
from pydantic import BaseModel

from app import schemas
from app.api.data.data_loader import *

router = APIRouter()


@router.post("/")
def backtest(item: schemas.backtest):
    json_request = item.dict()
    portfolio = json_request["portfolio"]
    fund_codes = []
    for i in portfolio:
        fund_codes.append(i["fund"])
    start_date = json_request["startDate"]
    end_date = json_request["endDate"]
    historicalData = loadHistoricalData(
        fund_codes=fund_codes, start_date=start_date, end_date=end_date
    )
    return historicalData
