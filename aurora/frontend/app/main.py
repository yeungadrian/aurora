import streamlit as st
from pages.home import display_home
from pages.backtest import display_backtest
from pages.factorRegression import display_factorRegression
from pages.portfolioOptimisation import display_portfolioOptimsiation

st.sidebar.title("Aurora")

appOptions = [
    "Home",
    "Portfolio backtesting",
    "Factor regression",
    "Portfolio optimisation",
]

currentPage = st.sidebar.radio("", appOptions)

if currentPage == appOptions[0]:
    display_home()

if currentPage == appOptions[1]:
    display_backtest()

if currentPage == appOptions[2]:
    display_factorRegression()

if currentPage == appOptions[3]:
    display_portfolioOptimsiation()
