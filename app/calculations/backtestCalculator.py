import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np


def backmodel(
    fund_amount,
    fund_list,
    fund_index,
):
    dates = fund_index["date"]
    num_funds = len(fund_list)
    fund_diag = np.zeros((num_funds, num_funds))
    np.fill_diagonal(fund_diag, fund_amount)
    result = fund_index[fund_list].dot(fund_diag)
    result.columns = fund_list
    result["portfolio"] = result.sum(axis=1)
    result["date"] = dates
    return result


def backTestModel(historical_index, portfolio, strategy, start_date, end_date):
    fund_index = pd.DataFrame(historical_index)
    fund_list = []
    fund_amount = []
    for i in portfolio:
        fund_list.append(i["fund"])
        fund_amount.append(i["amount"])

    if strategy["rebalance"]:
        fund_percentage = [i / sum(fund_amount) for i in fund_amount]
        frequency = {"y": 12, "q": 3, "m": 1}
        start_period = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        delta_months = relativedelta(end_date, start_period)

        diff_months = delta_months.months
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
            temp_dates = subset_index["date"]
            temp_df = backmodel(temp_amount, fund_list, subset_index)
            temp_total = temp_df.iloc[(temp_df.shape[0] - 1)].sum()
            temp_amount = [temp_total * i for i in fund_percentage]
            temp_df["date"] = temp_dates
            subset_list.append(temp_df)
            start_period = datetime.strptime(end_period, "%Y-%m-%d")

        result_df = pd.concat(subset_list)
        result_df["portfolio"] = result_df[fund_list]

    else:
        result_df = backmodel(fund_amount, fund_list, fund_index)

    return json.loads(result_df.to_json(orient="records"))
