from fastapi import APIRouter

from app import schemas
from app.data.dataLoader import load_historical_returns, load_ffFactors
import pandas as pd
import statsmodels.formula.api as smf
import json

router = APIRouter()


@router.post("/")
def factorRegression(item: schemas.factorRegression):

    fund_codes = item.dict()["funds"]
    start_date = item.dict()["startDate"]
    end_date = item.dict()["endDate"]
    regression_factors = item.dict()["regressionFactors"]

    historical_returns = pd.DataFrame(
        load_historical_returns(
            fund_codes=fund_codes,
            start_date=start_date,
            end_date=end_date,
        )
    )

    frenchfama_Factors = pd.DataFrame(
        load_ffFactors(
            regression_factors=regression_factors,
            start_date=start_date,
            end_date=end_date,
        )
    )

    regression_equation = " + ".join(regression_factors)

    historical_returns = historical_returns.set_index("date")
    historical_returns.index.name = None

    frenchfama_Factors = frenchfama_Factors.set_index("date")
    frenchfama_Factors.index.name = None

    regression_data = pd.concat([historical_returns, frenchfama_Factors], axis=1, join='inner')

    for i in fund_codes:
        regression_data[i] = regression_data[i] - regression_data["RF"]

    fund_code = fund_codes[0]

    model = smf.ols(
        formula=f"{fund_code} ~ {regression_equation}", data=regression_data
    )

    results = model.fit()

    coeff = results.params

    return json.loads(pd.DataFrame({"coefficients": coeff}).to_json())
