import streamlit as st
from pages.home import display_home
from pages.backtest import display_backtest
from pages.factorRegression import display_factorRegression

st.sidebar.title("Aurora")

appOptions = ["Home", "Portfolio backtesting", "Factor regression"]

currentPage = st.sidebar.radio("", appOptions)

if currentPage == "Home":
    display_home()

if currentPage == "Portfolio backtesting":
    display_backtest()

if currentPage == "Factor regression":
    display_factorRegression()
