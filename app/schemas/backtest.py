from pydantic import BaseModel


class backtest(BaseModel):
    startDate: str
    endDate: str
    portfolio: list
    benchmark: str= None
    strategy: dict

    class Config:
        schema_extra = {
            "example": {
                "startDate": "2018-12-31",
                "endDate": "2020-06-30",
                "portfolio": [
                    {
                        "fund": "MMM",
                        "amount": 1000
                    },
                    {
                        "fund": "ABT",
                        "amount": 1000
                    }
                ],
                "benchmark": "AAPL",
                "strategy": {
                    "rebalance": True,
                    "rebalanceFrequency": "Y"
                }
            }
        }