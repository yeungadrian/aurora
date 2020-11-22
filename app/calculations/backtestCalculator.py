import pandas as pd
import json


def backTestModel(historical_index, portfolio, strategy):
    fund_list = []
    fund_index = pd.DataFrame(historical_index)
    for i in portfolio:
        fund_list.append(i["fund"])

        if strategy["rebalance"]:
            # something more complex
            None
        else:
            fund_index[i["fund"]] = fund_index[i["fund"]] * i["amount"]
    fund_index["portfolio"] = fund_index[fund_list].sum(axis=1)
    return json.loads(fund_index[["date", "portfolio"]].to_json(orient="records"))
