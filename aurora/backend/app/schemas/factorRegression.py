from pydantic import BaseModel


class factorRegression(BaseModel):
    startDate: str
    endDate: str
    funds: list
    regressionFactors: list

    class Config:
        schema_extra = {
            "example": {
                "startDate": "2017-12-31",
                "endDate": "2019-12-31",
                "funds": ["AAPL"],
                "regressionFactors": ["MktRF", "SMB", "HML"],
            }
        }
