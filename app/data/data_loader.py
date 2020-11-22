import pandas as pd
import json


def loadHistoricalReturns(fund_codes, start_date, end_date):
    response_columns = fund_codes
    response_columns = ['date'] + fund_codes
    all_historical_prices = pd.read_csv("app/data/output.csv")
    subset_data = all_historical_prices[response_columns][
        all_historical_prices["date"] >= start_date
    ][all_historical_prices["date"] <= end_date]
    subset_data = subset_data.sort_values("date").reset_index(drop=True)
    for i in fund_codes:
        subset_data[f"{i}_return"] = subset_data[i] / subset_data[i].shift(1) - 1
        subset_data = subset_data.fillna(0)
    subset_data = subset_data.fillna(0)
    subset_data = subset_data.drop(fund_codes, axis=1)
    subset_data.columns = response_columns
    return json.loads(subset_data.to_json(orient="records"))
