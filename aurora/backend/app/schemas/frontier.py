from pydantic import BaseModel


class frontier(BaseModel):
    startDate: str
    endDate: str
    funds: list
    numberOfPortfolios: int

    class Config:
        schema_extra = {
            "example": {
                "startDate": "2015-12-31",
                "endDate": "2019-12-31",
                "funds": ["AAPL", "AMZN", "AMD"],
                "numberOfPortfolios": 4,
            }
        }
