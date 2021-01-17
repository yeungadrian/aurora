import pandas as pd
import statsmodels.formula.api as smf
import json


def calculatefactorRegression(
    fund_code,
    regression_factors,
    historical_returns,
    frenchfama_Factors,
):

    regression_equation = " + ".join(regression_factors)

    historical_returns = historical_returns.set_index("date")
    historical_returns.index.name = None

    frenchfama_Factors = frenchfama_Factors.set_index("date")
    frenchfama_Factors.index.name = None

    regression_data = pd.concat(
        [historical_returns, frenchfama_Factors], axis=1, join="inner"
    )

    regression_data[fund_code] = regression_data[fund_code] - regression_data["RF"]

    model = smf.ols(
        formula=f"{fund_code} ~ {regression_equation}", data=regression_data
    )

    results = model.fit()

    output = get_summary_results(results, fund_code)

    return output


def get_summary_results(results, fund_code):
    """take the result of an statsmodel results table and transforms it into a dataframe
    https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html"""

    accuracy = 6

    pvals = [round(elem, accuracy) for elem in (results.pvalues * 100)]
    coefficient = [round(elem, accuracy) for elem in (results.params * 100)]
    conf_lower = [round(elem, accuracy) for elem in (results.conf_int()[0] * 100)]
    conf_higher = [round(elem, accuracy) for elem in (results.conf_int()[1] * 100)]
    
    num_obs = round(results.nobs, accuracy)
    rsquared = round(results.rsquared, accuracy)
    rsquard_adj = round(results.rsquared_adj, accuracy)
    fvalue = round(results.fvalue, accuracy)

    output_result = {
        "fundCode": fund_code,
        "numberObservations": num_obs,
        "rSquared": rsquared,
        "rSquaredAdjusted": rsquard_adj,
        "fValue": fvalue,
        "coefficient": coefficient,
        "pValues": pvals,
        "confidenceIntervalLower": conf_lower,
        "confidenceIntervalHigher": conf_higher,
    }

    return output_result
