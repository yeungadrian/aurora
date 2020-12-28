import pandas as pd
from datetime import datetime
import numpy as np

def calculate_metrics(portfolio):
    portfolio = pd.DataFrame(portfolio)
    start_value = portfolio['portfolio'][0]
    end_value = portfolio['portfolio'].iat[-1]

    start_date = datetime.strptime(portfolio['date'][0],'%Y-%m-%d')
    end_date = datetime.strptime(portfolio['date'].iat[-1],'%Y-%m-%d')

    num_years = (end_date - start_date).days / 365.25

    print(start_value, end_value, num_years)

    cagr = calculate_cagr(end_value = end_value, start_value = start_value, num_years = num_years)

    #month_end_projection = portfolio[portfolio["date"].dt.is_month_end].reset_index(drop=True)
    #month_end_projection['monthlyReturns'] = month_end_projection['portfolio'] / month_end_projection['portfolio'].shift(-1) - 1

    result = {
        'cagr': cagr
    }

    return result

def calculate_cagr(end_value, start_value, num_years):

    return (end_value / start_value) ** (1 / num_years) - 1
