import streamlit as st
from pages.home import display_home
from pages.backtest import display_backtest

st.sidebar.title("Aurora")

appOptions = ["Home", "Portfolio backtesting"]

currentPage = st.sidebar.radio("", appOptions)

if currentPage == "Home":
    display_home()

if currentPage == "Portfolio backtesting":
    display_backtest()
