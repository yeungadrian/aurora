import flask
from flask import request, jsonify
import requests
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/backtest/', methods=['POST'])
def backtest():

    json_request = request.get_json()
    allocation_weights = json_request['allocation_weights']
    initial_amount = json_request['initial_amount']
    start_date = json_request['start_date']
    end_date = json_request['end_date']
    codelist = json_request['codelist']
    benchmark = json_request['benchmark']

    rebalance = json_request['rebalance']
    rebalance_frequency = json_request['rebalance_frequency']
    alpha_key = json_request['alpha_key']

    indexdata = pd.DataFrame()

    alpha_code = codelist
    if benchmark != 'None':
        alpha_code = codelist + [benchmark]

    for x in range(0,len(alpha_code)):
        alpha_request = (
        'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol='
        f'{alpha_code[0]}&outputsize=full&apikey={alpha_key}'
        )
        response = requests.get(alpha_request).json()
        
        response_df = pd.DataFrame(response['Time Series (Daily)']).transpose().reset_index()
        response_df['4. close'] = pd.to_numeric(response_df['4. close'])
        response_df = response_df[['index','4. close']]
        response_df = response_df[response_df['index']>start_date][response_df['index']<end_date]
        if x == len(alpha_code)-1:
            response_df.columns = ['date','benchmark']
        else:
            response_df.columns = ['date',alpha_code[x]]
        
        if x == 0:
            indexdata = indexdata.append(response_df)
        else:
            indexdata = pd.merge(indexdata,response_df)

    month_frequency = {
        'Yearly': 12,
        'Quarterly': 3,
        'Monthly': 1
    }

    end_date = datetime.strptime(end_date,'%Y-%m-%d')
    start_date = datetime.strptime(start_date,'%Y-%m-%d')
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if (end_date.day < start_date.day):
        num_months = num_months - 1

    event_count = int(math.floor(num_months / month_frequency[rebalance_frequency]))

    rebalance_list =[start_date.strftime("%Y-%m-%d")]
    if rebalance:
        rebalance_date = start_date
        for x in range(0,event_count):
            rebalance_date = rebalance_date + relativedelta(months=+month_frequency[rebalance_frequency])
            rebalance_list.append(rebalance_date.strftime("%Y-%m-%d"))
    else:
        rebalance_list.append(end_date.strftime("%Y-%m-%d"))

    asset_projection = []

    asset_value = [x * initial_amount for x in allocation_weights]

    for x in range(0,len(rebalance_list)-1):
        asset_value = [x * initial_amount for x in allocation_weights]
        
        index_subset = indexdata[indexdata['date'] >= rebalance_list[0+x]][indexdata['date'] < rebalance_list[1+x]]
        index_subset = index_subset.sort_values(by='date').reset_index(drop=True)

        allocation = pd.DataFrame()

        for i in range(0,len(allocation_weights)):
            indexcode = index_subset.columns[i+1]
            scaling_factor = asset_value[i] / index_subset[indexcode][0]
            allocation[f'allocation {i}'] = index_subset[indexcode] * scaling_factor
        
        asset_projection.append(allocation)
        
        asset_value = allocation.iloc[len(allocation)-1].sum()

    asset_projection = pd.concat(asset_projection).reset_index(drop=True)

    if benchmark != 'None':
        scaling_factor = initial_amount / indexdata.sort_values(by='date').reset_index(drop=True)['benchmark'][0]
        asset_projection['benchmark'] = indexdata.sort_values(by='date').reset_index(drop=True)['benchmark'] * scaling_factor

    asset_projection['output'] = asset_projection.sum(axis = 1)
    asset_projection['date'] = indexdata['date']

    output_field = ['date','output']

    if benchmark != 'None':
        output_field = output_field +['benchmark']
    return jsonify(json.loads(asset_projection[output_field].to_json(orient='records')))

app.run()