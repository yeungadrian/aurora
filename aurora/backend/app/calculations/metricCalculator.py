import pandas as pd
import numpy as np
import json


def calculate_metrics(portfolio):
    portfolio = pd.DataFrame(portfolio)
    portfolio["date"] = pd.to_datetime(portfolio["date"])

    start_value = portfolio["portfolio"][0]
    end_value = portfolio["portfolio"].iat[-1]

    start_date = portfolio["date"][0]
    end_date = portfolio["date"].iat[-1]

    # Number of years calculation could be improved, do difference in months and pretend always at end of month
    num_years = (end_date - start_date).days / 365.25

    # Needs to be dynamically loaded eventually
    risk_free = 0.01

    month_end_projection = portfolio[portfolio["date"].dt.is_month_end].reset_index(
        drop=True
    )

    month_end_projection["monthlyReturns"] = (
        month_end_projection["portfolio"].shift(1) / month_end_projection["portfolio"]
        - 1
    )

    monthly_returns = month_end_projection[["date", "monthlyReturns"]].dropna(
        axis="index"
    )
    monthly_returns["date"] = monthly_returns["date"].dt.strftime("%Y-%m-%d")
    monthly_returns = json.loads(monthly_returns.to_json(orient="records"))

    cagr = calculate_cagr(
        end_value=end_value, start_value=start_value, num_years=num_years
    )
    negative_returns = month_end_projection[month_end_projection["monthlyReturns"] < 0]
    monthly_std = calculate_std(returns=month_end_projection["monthlyReturns"])
    negative_std = calculate_std(returns=negative_returns["monthlyReturns"])

    sharpe_ratio = calculate_portfolio_ratio(
        portfolio_return=cagr, risk_free=risk_free, std=monthly_std
    )

    sortino_ratio = calculate_portfolio_ratio(
        portfolio_return=cagr, risk_free=risk_free, std=negative_std
    )

    result = {
        "cagr": cagr,
        "monthly_std": monthly_std,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "monthly_returns": monthly_returns,
    }

    return result


def calculate_cagr(end_value, start_value, num_years):

    return np.power(end_value / start_value, 1 / num_years) - 1


def calculate_std(returns):

    return np.std(returns)


def calculate_portfolio_ratio(portfolio_return, risk_free, std):
    return (portfolio_return - risk_free) / std
