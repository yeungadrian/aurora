from fastapi import APIRouter
from pydantic import BaseModel

from app import schemas

router = APIRouter()

@router.post("/")
def backtest1(item: schemas.backtest):
    return 'asd'