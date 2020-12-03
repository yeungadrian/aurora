import requests

def get_funds():
    url = 'http://api:8000/funds/'
    response = requests.get(url).json()

    return (response)

def backtest(json_input):
    url_backtest = 'http://api:8000/backtest/'
    response = requests.post(url = url_backtest, json = json_input).json()

    return response