from fastapi import FastAPI
from pydantic import BaseModel

import requests
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import json

class Item(BaseModel):
    codeList : list
    benchmark: str
    start_date : str
    end_date : str
    regressionFactors: list
    token: str

app = FastAPI()

def iexHistoricalPriceRequest (codeList,token):
    indexData = pd.DataFrame()
    codeListString = ','.join(codeList)
    iexRequest = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={codeListString}&types=chart&range=max&token={token}&filter=date,close'
    iexResponse = requests.get(iexRequest).json()
    for x in codeList:
        singleCode = pd.DataFrame(iexResponse[x]['chart'])
        singleCode.columns = ['date',x]
        if x == codeList[0]:
            indexData = indexData.append(singleCode)
        else:
            indexData = pd.merge(indexData,singleCode)
    indexData = indexData.sort_values(by='date').reset_index(drop=True)
    return(indexData)

def result_summary_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    #https://www.statsmodels.org/stable/generated/statsmodels.regression.linear_model.RegressionResults.html link if interested in adding more results
    summary_json = {
    'nobs': results.nobs,
    'rsquared': results.rsquared,
    'rsquared_adj': results.rsquared_adj,
    'fvalue': results.fvalue
    }
    return summary_json

def result_pvalues_to_dataframe(results):
    '''take the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = results.pvalues
    coeff = results.params
    conf_lower = results.conf_int()[0]
    conf_higher = results.conf_int()[1]

    results_df = pd.DataFrame({"pvals":pvals,
                               "coeff":coeff,
                               "conf_lower":conf_lower,
                               "conf_higher":conf_higher
                                })

    #Reordering...
    results_df = results_df[["coeff","pvals","conf_lower","conf_higher"]]
    return results_df

@app.post("/factorRegression/")
def factorRegression(item: Item):
    json_request = item.dict()
    start_date = json_request['start_date']
    end_date = json_request['end_date']
    codeList = json_request['codeList']
    benchmark = json_request['benchmark']
    regressionFactors= json_request['regressionFactors']
    token = json_request['token']

    codeList.append(benchmark)

    indexData = iexHistoricalPriceRequest(codeList,token)
    indexData=indexData.rename(columns = {indexData.columns[-1] :'benchmark'})
    indexData = indexData[indexData['date']>=start_date]
    indexData = indexData[indexData['date']<=end_date]
    indexData = indexData.reset_index(drop=True)

    indexData['portfolioreturn'] = (indexData[codeList[0]] - indexData[codeList[0]].shift(1))/indexData[codeList[0]].shift(1)
    indexData['benchmarkreturn'] = (indexData.benchmark - indexData.benchmark.shift(1))/indexData.benchmark.shift(1)

    frenchfama = pd.read_csv('data/ff5factordaily.CSV')
    frenchfama = frenchfama[frenchfama['date']>start_date]
    frenchfama = frenchfama[frenchfama['date']<=end_date].reset_index(drop=True)
    regression_data = pd.concat([indexData,frenchfama],axis = 1,join = 'inner')

    regressionFactors = ' + '.join(regressionFactors)

    model = smf.ols(formula=f'portfolioreturn ~ {regressionFactors}', data=regression_data)
    results = model.fit()

    pvaluesJSON = result_pvalues_to_dataframe(results).to_json()
    summaryJSON = result_summary_to_dataframe(results)
    pvaluesJSON = json.loads(pvaluesJSON)
    outputJSON = summaryJSON
    outputJSON.update(pvaluesJSON)

    return (outputJSON)
