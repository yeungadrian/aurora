from fastapi import APIRouter
from pydantic import BaseModel

from app import schemas
from app.api.data import loadHistoricalData

router = APIRouter()


@router.post("/")
def backtest(item: schemas.backtest):

    historicalData = loadHistoricalData()
    return "asd"
