from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

import pandas as pd
import json
import numpy as np
from scipy.optimize import minimize

router = APIRouter()


class optimizeItem(BaseModel):
    optimization: Dict
    portfolio: list


@router.post("/")
def optimizeFactor(item: optimizeItem):
    json_request = item.dict()
    factorSet = json_request['portfolio']
    optimizationParameters = json_request['optimization']

    factorData = pd.DataFrame()
    for y in range(0, len(factorSet)):
        if y == 0:
            factorData = pd.DataFrame(factorSet[y])
        else:
            factorData = factorData.join(pd.DataFrame(factorSet[y]))

    x0 = np.array(factorData.loc['initialweight'])

    def rosen(x):
        lossFunction = []
        for i in range(0, len(optimizationParameters.keys())):
            currentFactor = list(optimizationParameters.keys())[i]
            target = optimizationParameters[currentFactor]
            currentFactorValues = np.array(factorData.loc[currentFactor])
            currentValue = np.multiply(x, currentFactorValues).sum()
            lossFunction.append((target - currentValue) ** 2)
        return np.array(lossFunction).sum()

    def constraint(x):
        return np.sum(x) - 1

    bounds = ()
    for j in range(0, len(optimizationParameters.keys())):
        bounds = bounds + ((0, 1),)

    result = minimize(rosen, x0, method='SLSQP',
                      constraints={"fun": constraint, "type": "eq"},
                      options={'disp': False})

    return list(result.x)
