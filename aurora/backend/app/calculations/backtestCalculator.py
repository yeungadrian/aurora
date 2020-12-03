import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np


def backtest_funds(
    fund_amount,
    fund_codes,
    fund_index,
):
    num_funds = len(fund_codes)

    fund_diag = np.zeros((num_funds, num_funds))
    np.fill_diagonal(fund_diag, fund_amount)

    result = fund_index[fund_codes].dot(fund_diag)
    result.columns = fund_codes
    
    result["portfolio"] = result.sum(axis=1)

    return result


def backtest_strategy(historical_index, portfolio, strategy, start_date, end_date):
    fund_index = pd.DataFrame(historical_index)
    fund_codes = []
    fund_amount = []
    for i in portfolio:
        fund_codes.append(i["fund"])
        fund_amount.append(i["amount"])
    
    dates = fund_index["date"]

    if strategy["rebalance"]:
        fund_percentage = [i / sum(fund_amount) for i in fund_amount]
        frequency = {"y": 12, "q": 3, "m": 1}
        start_period = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        delta_months = relativedelta(end_date, start_period)

        # To Do: Test edge cases of the rebalancing / dates, e.g. Leap Years, Weekends

        diff_months = delta_months.months + delta_months.years * 12
        if delta_months.days != 0:
            diff_months = diff_months + 1

        rebalanceFrequency = strategy["rebalanceFrequency"].lower()

        temp_amount = fund_amount
        subset_list = []
        for j in range(0, diff_months):
            end_period = start_period + relativedelta(
                months=frequency[rebalanceFrequency]
            )
            start_period = start_period.strftime("%Y-%m-%d")
            end_period = end_period.strftime("%Y-%m-%d")

            subset_index = fund_index[fund_index["date"] >= start_period][
                fund_index["date"] <= end_period
            ]
            for k in fund_codes:
                subset_index[k] = (
                    subset_index[k] / subset_index[k][subset_index.index[0]]
                )
            temp_dates = subset_index["date"]

            temp_df = backtest_funds(temp_amount, fund_codes, subset_index)
            temp_total = temp_df.iloc[(temp_df.shape[0] - 1)].sum()
            temp_amount = [temp_total * i for i in fund_percentage]
            temp_df["date"] = temp_dates

            start_period = datetime.strptime(
                temp_df["date"][temp_df.index[-1]], "%Y-%m-%d"
            )

            temp_df.drop(temp_df.tail(1).index, inplace=True)
            subset_list.append(temp_df)

        result_df = pd.concat(subset_list)
      
    else:
        result_df = backtest_funds(fund_amount, fund_codes, fund_index)
        result_df["date"] = dates

    return json.loads(result_df.to_json(orient="records"))
