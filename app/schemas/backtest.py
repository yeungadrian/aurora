from pydantic import BaseModel


class backtest(BaseModel):
    startDate: str
    endDate: str
    portfolio: list
    benchmark: str
    strategy: dict
