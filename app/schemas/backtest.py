from pydantic import BaseModel

class backtest(BaseModel):
    allocation_weights: list
