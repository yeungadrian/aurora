import pandas as pd
import json


def loadHistoricalData(fund_codes, startDate, endDate):
    fund_codes.insert(0, "date")
    all_historical_prices = pd.read_csv("output.csv")
    subset_data = all_historical_prices[fund_codes][
        all_historical_prices["date"] >= startDate
    ][all_historical_prices["date"] <= endDate]
    subset_data = subset_data.sort_values("date").reset_index(drop=True)
    return json.loads(subset_data.to_json(orient="records"))
