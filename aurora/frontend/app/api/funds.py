import requests
import streamlit as st


@st.cache()
def get_funds():
    url = "http://api:8000/funds/"
    response = requests.get(url).json()

    return response


@st.cache()
def backtest(json_input):
    url_backtest = "http://api:8000/backtest/"
    response = requests.post(url=url_backtest, json=json_input).json()

    return response


@st.cache()
def factorRegression(json_input):
    url_factorRegression = "http://api:8000/factorRegression/"
    response = requests.post(url=url_factorRegression, json=json_input).json()

    return response


@st.cache()
def efficientFrontier(json_input):
    url_efficientFrontier = "http://api:8000/portfolioOptimisation/"
    response = requests.post(url=url_efficientFrontier, json=json_input).json()

    return response
