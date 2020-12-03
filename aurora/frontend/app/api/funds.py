import requests

def get_funds():
    url = 'http://api:8000/funds/'
    Response = requests.get(url).json()
    fundList = []
    for x in range(0, len(Response)):
        fundList.append(Response[x]['Code'])
    return (fundList)