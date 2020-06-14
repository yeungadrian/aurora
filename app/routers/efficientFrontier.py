from fastapi import APIRouter
from pydantic import BaseModel

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math
import json
import numpy as np
import scipy.optimize as sco

router = APIRouter()


class efficientFrontierItem(BaseModel):
    codelist: list
    start_date: str
    end_date: str

class simulatedFrontierItem(BaseModel):
    codelist: list
    start_date: str
    end_date: str
    num_portfolios: int


@router.post("/individualReturns")
def individualReturns(item: efficientFrontierItem):
    json_request = item.dict()
    codeList = json_request['codelist']
    start_date = json_request['start_date']
    end_date = json_request['end_date']

    indexData = pd.read_csv('data/output.csv')

    indexColumns = ['date']+codeList
    indexData = indexData[indexColumns]
 
    indexData = indexData[indexData['date'] >= start_date]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)

    for x in range(0,len(codeList)):
        indexData[f'{codeList[x]}returns'] = indexData[f'{codeList[x]}'].pct_change()

    indexDataAltair = pd.DataFrame()

    for x in range(0,len(codeList)):
        tempAltair = indexData[['date',codeList[x],f'{codeList[x]}returns']]
        tempAltair.columns = ['date','price','returns']
        tempAltair['symbol'] = codeList[x]
        indexDataAltair = indexDataAltair.append(tempAltair)

    indexDataAltair = indexDataAltair.reset_index(drop=True)

    output = json.loads(indexDataAltair.to_json())

    return(output)

@router.post("/simulatedFrontier")
def simulatedFrontier(item: simulatedFrontierItem):
    json_request = item.dict()
    codeList = json_request['codelist']
    start_date = json_request['start_date']
    end_date = json_request['end_date']
    num_portfolios = json_request['num_portfolios']

    indexData = pd.read_csv('data/output.csv')

    indexColumns = ['date']+codeList
    indexData = indexData[indexColumns]
 
    indexData = indexData[indexData['date'] >= start_date]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)

    for x in range(0,len(codeList)):
        indexData[f'{codeList[x]}returns'] = indexData[f'{codeList[x]}'].pct_change()

    indexDataAltair = pd.DataFrame()
    returnList = []

    for x in range(0,len(codeList)):
        tempAltair = indexData[['date',codeList[x],f'{codeList[x]}returns']]
        tempAltair.columns = ['date','price','returns']
        tempAltair['symbol'] = codeList[x]
        indexDataAltair = indexDataAltair.append(tempAltair)
        returnList.append(f'{codeList[x]}returns')

    indexDataAltair = indexDataAltair.reset_index(drop=True)

    def get_annual_portfolio_performance(weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights ) * 252
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        return volatility, returns

    def generate_random_portfolios(num_portfolios, num_funds, mean_returns, cov_matrix, risk_free):
        results = np.zeros((3,num_portfolios))
        weights_List = []
        for i in range(num_portfolios):
            weights = np.random.random(num_funds)
            weights /= np.sum(weights)
            weights_List.append(weights)
            portfolio_stdev, portfolio_return = get_annual_portfolio_performance(weights, mean_returns, cov_matrix)
            results[0,i] = portfolio_stdev
            results[1,i] = portfolio_return
            results[2,i] = (portfolio_return - risk_free) / portfolio_stdev
        return results, weights_List

    returns = indexData[returnList]
    returns.columns = codeList
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    risk_free = 0.0178
    num_funds = len(codeList)

    results, weights = generate_random_portfolios(num_portfolios,num_funds,mean_returns, cov_matrix, risk_free)

    results_DF = pd.DataFrame(results).transpose()
    results_DF.columns = ['Volatility','Return','Sharpe Ratio']

    weightsDF = pd.DataFrame(weights)
    weightsDF.columns = codeList

    results_DF[codeList] = weightsDF

    output = json.loads(results_DF.to_json())

    return(output)

@router.post("/efficientFrontier")
def EfficientFrontier(item: efficientFrontierItem):
    json_request = item.dict()
    codeList = json_request['codelist']
    start_date = json_request['start_date']
    end_date = json_request['end_date']

    indexData = pd.read_csv('data/output.csv')

    indexColumns = ['date']+codeList
    indexData = indexData[indexColumns]
 
    indexData = indexData[indexData['date'] >= start_date]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)

    for x in range(0,len(codeList)):
        indexData[f'{codeList[x]}returns'] = indexData[f'{codeList[x]}'].pct_change()

    indexDataAltair = pd.DataFrame()
    returnList = []

    for x in range(0,len(codeList)):
        tempAltair = indexData[['date',codeList[x],f'{codeList[x]}returns']]
        tempAltair.columns = ['date','price','returns']
        tempAltair['symbol'] = codeList[x]
        indexDataAltair = indexDataAltair.append(tempAltair)
        returnList.append(f'{codeList[x]}returns')

    indexDataAltair = indexDataAltair.reset_index(drop=True)

    def get_annual_portfolio_performance(weights, mean_returns, cov_matrix):
        returns = np.sum(mean_returns * weights ) * 252
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        return volatility, returns

    returns = indexData[returnList]
    returns.columns = codeList
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    risk_free = 0.0178
    num_funds = len(codeList)
    
    def portfolio_volatility(weights, mean_returns, cov_matrix):
        return get_annual_portfolio_performance(weights, mean_returns, cov_matrix)[0]

    def efficient_return(mean_returns, cov_matrix, target, num_funds):
        args = (mean_returns, cov_matrix)

        def portfolio_return(weights):
            return get_annual_portfolio_performance(weights, mean_returns, cov_matrix)[1]

        constraints = ({'type': 'eq', 'fun': lambda x: portfolio_return(x) - target},
                    {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = tuple((0,1) for asset in range(num_funds))
        result = sco.minimize(portfolio_volatility, num_funds*[1./num_funds,], args=args, method='SLSQP', bounds=bounds, constraints=constraints)
        return result


    def efficient_frontier(mean_returns, cov_matrix, returns_range):
        efficients = []
        for ret in returns_range:
            efficients.append(efficient_return(mean_returns, cov_matrix, ret, num_funds))
        return efficients

    def min_variance(mean_returns, cov_matrix, num_funds):
        args = (mean_returns, cov_matrix)
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bound = (0.0,1.0)
        bounds = tuple(bound for asset in range(num_funds))

        result = sco.minimize(portfolio_volatility, num_funds*[1./num_funds,], args=args,
                            method='SLSQP', bounds=bounds, constraints=constraints)

        return result
    
    min_vol = min_variance(mean_returns, cov_matrix, num_funds)
    mid_stdev, min_return = get_annual_portfolio_performance(min_vol['x'], mean_returns, cov_matrix)
    num_efficient_portfolios = 50
    target = np.linspace(min_return, max(mean_returns)* 252, num_efficient_portfolios)

    efficient_portfolios = efficient_frontier(mean_returns, cov_matrix, target)

    output = pd.DataFrame(efficient_portfolios)
    output = output[['x','fun']]
    output['target'] = pd.DataFrame(target)
    output.columns = ['weights','Volatility','Return']
    output['Sharpe Ratio'] = (output['Return'] - risk_free) / output['Volatility']

    for y in range(0,len(codeList)):
        temporaryList = []
        for x in range(0,num_efficient_portfolios):
            temporaryList.append(output['weights'][x][y])
        output[codeList[y]] = temporaryList

    del output['weights']
    
    output = output.to_json()

    return json.loads(output)

@router.post("/meanvariance")
def EfficientFrontier(item: efficientFrontierItem):
    json_request = item.dict()
    codeList = json_request['codelist']
    start_date = json_request['start_date']
    end_date = json_request['end_date']

    indexData = pd.read_csv('data/output.csv')

    indexColumns = ['date']+codeList
    indexData = indexData[indexColumns]
 
    indexData = indexData[indexData['date'] >= start_date]
    indexData = indexData.sort_values(by='date').reset_index(drop=True)

    for x in range(0,len(codeList)):
        indexData[f'{codeList[x]}returns'] = indexData[f'{codeList[x]}'].pct_change()
    
    indexDataAltair = pd.DataFrame()
    returnList = []

    for x in range(0,len(codeList)):
        tempAltair = indexData[['date',codeList[x],f'{codeList[x]}returns']]
        tempAltair.columns = ['date','price','returns']
        tempAltair['symbol'] = codeList[x]
        indexDataAltair = indexDataAltair.append(tempAltair)
        returnList.append(f'{codeList[x]}returns')

    indexDataAltair = indexDataAltair.reset_index(drop=True)

    returns = indexData[returnList]
    returns.columns = codeList
    cov_matrix = returns.cov()

    volatilitylist = {}
    for y in range(0,len(codeList)):
        listofzeros = [0] * len(codeList)
        listofzeros[y] = 1
        listofzeros = np.array(listofzeros)
        volatility_temp = np.sqrt(np.dot(listofzeros.T, np.dot(cov_matrix, listofzeros))) * np.sqrt(252)
        volatilitylist[codeList[y]] = volatility_temp

    mean_returns = returns.mean() * 252
    mean_returns = pd.DataFrame(mean_returns).reset_index()
    mean_returns.columns = ['index','Return']
    volatility = pd.DataFrame(volatilitylist, index = [0]).transpose().reset_index()

    volatility.columns = ['index','Volatility']
    output = pd.concat([mean_returns,volatility],axis = 1, sort = False)

    output.columns = ['Symbol','Return','Index','Volatility']

    del output['Index']

    return output