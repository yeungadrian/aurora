import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

from api.funds import get_funds, backtest


def display_backtest():

    st.title("Portfolio Backtesting")
    fund_list = pd.DataFrame(get_funds())

    with st.beta_expander(label="Portfolio inputs"):

        date_col1, date_col2 = st.beta_columns(2)

        start_date = date_col1.date_input(
            "Start Date", value=datetime(2018, 12, 31)
        ).strftime("%Y-%m-%d")
        end_date = date_col2.date_input(
            "End Date", value=datetime(2020, 3, 31)
        ).strftime("%Y-%m-%d")

        rebalance_options = {"Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}

        rebalance = date_col1.checkbox("Rebalance portfolio")
        if rebalance:
            rebalance_frequency = date_col2.selectbox(
                label="Rebalance frequency", options=list(rebalance_options.keys())
            )
            frequency = rebalance_options[rebalance_frequency]
        else:
            frequency = None

        selected_funds = st.multiselect(
            label="Fund selection", options=list(fund_list["Company"])
        )
        portfolio = []
        amount_list = []
        for i in range(0, len(selected_funds)):
            amount = st.number_input(label=f" {selected_funds[i]}", key=i)
            amount_list.append(amount)

        for i in range(0, len(selected_funds)):
            portfolio.append(
                {
                    "fund": fund_list[fund_list["Company"] == selected_funds[i]][
                        "Code"
                    ].reset_index(drop=True)[0],
                    "amount": amount_list[i],
                }
            )

    if len(portfolio):
        backtest_input = {
            "startDate": start_date,
            "endDate": end_date,
            "portfolio": portfolio,
            "benchmark": "AAPL",
            "strategy": {"rebalance": rebalance, "rebalanceFrequency": frequency},
        }

        backtest_portfolio = pd.DataFrame(backtest(backtest_input))
        backtest_portfolio["date"] = pd.to_datetime(backtest_portfolio["date"])

        with st.beta_expander(label="Portfolio historical projection"):

            chartoutput = (
                alt.Chart(backtest_portfolio)
                .mark_line()
                .encode(x="date", y="portfolio")
                .properties(width=700)
            )

            st.write(chartoutput)
