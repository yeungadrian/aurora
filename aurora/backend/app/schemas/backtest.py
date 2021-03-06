from pydantic import BaseModel


class backtest(BaseModel):
    startDate: str
    endDate: str
    portfolio: list
    strategy: dict

    class Config:
        schema_extra = {
            "example": {
                "startDate": "2018-12-31",
                "endDate": "2020-06-30",
                "portfolio": [
                    {"fund": "ABMD", "amount": 1000},
                    {"fund": "ATVI", "amount": 1000},
                ],
                "strategy": {"rebalance": True, "rebalanceFrequency": "Y"},
            }
        }
