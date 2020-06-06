from fastapi import APIRouter
from pydantic import BaseModel

import pandas as pd
import numpy as np
import json
from statsmodels.tsa.stattools import coint
from itertools import combinations
from datetime import datetime
from dateutil.relativedelta import relativedelta

router = APIRouter()


class assetAnalysisItem(BaseModel):
    codelist: list
    start_date: str
    end_date: str

@router.post("/correlation")
def correlation(item: assetAnalysisItem):
    json_request = item.dict()

    start_date = json_request['start_date']
    end_date = json_request['end_date']
    codelist = json_request['codelist']

    indexData = pd.read_csv('data/output.csv')
    indexData = indexData[['date'] + codelist]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)

    indexData = indexData[indexData['date'] >= start_date]
    indexData = indexData[indexData['date'] <= end_date]
    indexData = indexData.reset_index(drop=True)

    correlationMatrix = indexData.corr()
    correlationMatrixJSON = correlationMatrix.to_json()
    for x in codelist:
        indexData[x] = (indexData[x] - indexData[x].shift(1))/indexData[x].shift(1)

    indexDatastd = indexData.std(axis = 0)

    outputJSON = {}
    outputJSON['correlation'] = json.loads(correlationMatrixJSON)
    outputJSON['std'] = indexDatastd

    return outputJSON

@router.post("/rollingCorrelation")
def rollingCorrelation(item: assetAnalysisItem):

    json_request = item.dict()

    start_date = json_request['start_date']
    end_date = json_request['end_date']
    codelist = json_request['codelist']

    indexData = pd.read_csv('data/output.csv')
    indexData = indexData[['date'] + codelist]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)
    #Rolling Correlation
    
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    rollingMonths = [start_date]
    rollingDate = start_date
    for x in range(0, num_months):
        rollingDate = rollingDate + relativedelta(months=+1)
        rollingMonths.append(rollingDate)

    rollingJSON = {}

    for x in rollingMonths:
        endDate = x
        startDate = x + relativedelta(months=-36)
        endDate = f'{endDate:%Y-%m-%d}'
        startDate = f'{startDate:%Y-%m-%d}'
        correlationData = indexData[indexData['date'] >= startDate]
        correlationData = correlationData[correlationData['date'] <= endDate]
        correlationMatrix = correlationData.corr()
        rollingJSON[endDate] = correlationMatrix[codelist[0]][codelist[1]]

    return rollingJSON




@router.post("/cointegration")
def cointegration(item: assetAnalysisItem):
    json_request = item.dict()

    start_date = json_request['start_date']
    end_date = json_request['end_date']
    codelist = json_request['codelist']

    indexData = pd.read_csv('data/output.csv')
    indexData = indexData[['date'] + codelist]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)

    indexData = indexData[indexData['date'] >= start_date]
    indexData = indexData[indexData['date'] <= end_date]
    indexData = indexData.reset_index(drop=True)

    uniquePairs = list(combinations(codelist, r = 2))

    for x in range(0,len(uniquePairs)):

        y0 = indexData[uniquePairs[x][0]]
        y1 = indexData[uniquePairs[x][1]]

        cointegrationResult = coint(y0, y1, trend='ct', method='aeg', autolag='aic', return_results = True)
        intermediatePair = {
            str(x):
            {
                "Dependent": uniquePairs[x][0],
                "Independent": uniquePairs[x][1],
                "Test Statistic": cointegrationResult[0],
                "p-value": cointegrationResult[1]
            }
        }

        intermediateDataFrame = (pd.DataFrame(intermediatePair).transpose())
        if x == 0:
            cointegrationDataFrame = intermediateDataFrame
        else: 
            cointegrationDataFrame = pd.concat([cointegrationDataFrame, intermediateDataFrame])

    cointegrationJSON = cointegrationDataFrame.to_json(orient = 'records')

    return json.loads(cointegrationJSON)

