import pandas as pd
import json


def loadHistoricalData(fund_codes, start_date, end_date):
    fund_codes.insert(0, "date")
    all_historical_prices = pd.read_csv("app/api/data/output.csv")
    subset_data = all_historical_prices[fund_codes][
        all_historical_prices["date"] >= start_date
    ][all_historical_prices["date"] <= end_date]
    subset_data = subset_data.sort_values("date").reset_index(drop=True)
    return json.loads(subset_data.to_json(orient="records"))
