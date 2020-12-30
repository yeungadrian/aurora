import pandas as pd
import numpy as np


def calculate_metrics(portfolio):
    portfolio = pd.DataFrame(portfolio)
    portfolio["date"] = pd.to_datetime(portfolio["date"])

    start_value = portfolio["portfolio"][0]
    end_value = portfolio["portfolio"].iat[-1]

    start_date = portfolio["date"][0]
    end_date = portfolio["date"].iat[-1]
    num_years = (end_date - start_date).days / 365.25

    month_end_projection = portfolio[portfolio["date"].dt.is_month_end].reset_index(
        drop=True
    )
    month_end_projection["monthlyReturns"] = (
        month_end_projection["portfolio"] / month_end_projection["portfolio"].shift(-1)
        - 1
    )

    cagr = calculate_cagr(
        end_value=end_value, start_value=start_value, num_years=num_years
    )
    
    monthly_std = calculate_std(returns=month_end_projection["monthlyReturns"])

    result = {"cagr": cagr, "monthly_std": monthly_std}

    return result


def calculate_cagr(end_value, start_value, num_years):

    return np.power(end_value / start_value, 1 / num_years) - 1


def calculate_std(returns):

    return np.std(returns)
