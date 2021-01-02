import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

from api.funds import get_funds, backtest


def display_backtest():

    # Portfolio Backtesting

    st.title("Portfolio Backtesting")
    fund_list = pd.DataFrame(get_funds())

    st.sidebar.subheader("Portfolio inputs")

    start_date = st.sidebar.date_input(
        "Start Date", value=datetime(2018, 12, 31)
    ).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End Date", value=datetime(2020, 3, 31)).strftime(
        "%Y-%m-%d"
    )

    rebalance_options = {"Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}

    rebalance = st.sidebar.checkbox("Rebalance portfolio")
    if rebalance:
        rebalance_frequency = st.sidebar.selectbox(
            label="Rebalance frequency", options=list(rebalance_options.keys())
        )
        frequency = rebalance_options[rebalance_frequency]
    else:
        frequency = None

    selected_funds = st.sidebar.multiselect(
        label="Fund selection", options=list(fund_list["Company"])
    )
    portfolio = []
    amount_list = {}
    for i in range(0, len(selected_funds)):
        amount_list[f"fund{i}"] = st.sidebar.number_input(
            label=f"{selected_funds[i]}", key=i
        )

    for i in range(0, len(selected_funds)):
        portfolio.append(
            {
                "fund": fund_list[fund_list["Company"] == selected_funds[i]][
                    "Code"
                ].reset_index(drop=True)[0],
                "amount": amount_list[f"fund{i}"],
            }
        )

    # Portfolio Historical Projection

    if len(portfolio):
        backtest_input = {
            "startDate": start_date,
            "endDate": end_date,
            "portfolio": portfolio,
            "strategy": {"rebalance": rebalance, "rebalanceFrequency": frequency},
        }

        backtest_response = backtest(backtest_input)

        backtest_portfolio = pd.DataFrame(backtest_response["projection"])
        backtest_portfolio["date"] = pd.to_datetime(backtest_portfolio["date"])

        with st.beta_expander(label="Portfolio historical projection"):

            chartoutput = (
                alt.Chart(backtest_portfolio)
                .mark_line()
                .encode(x="date", y="portfolio")
                .properties(width=700)
            )

            st.write(chartoutput)

        with st.beta_expander(label="Metrics"):
            metrics_list = ["cagr", "monthly_std", "sharpe_ratio", "sortino_ratio"]
            metrics_table = dict(
                (k, backtest_response["metrics"][k])
                for k in metrics_list
                if k in backtest_response["metrics"]
            )
            st.write(pd.DataFrame(metrics_table, index=[0]))

        with st.beta_expander(label="Monthly returns"):
            monthly_return_chart = (
                alt.Chart(pd.DataFrame(backtest_response["metrics"]["monthly_returns"]))
                .mark_bar()
                .encode(x="date", y="monthlyReturns")
                .properties(width=700)
            )

            st.write(monthly_return_chart)

        with st.beta_expander(label="Daily drawdown"):
            monthly_return_chart = (
                alt.Chart(pd.DataFrame(backtest_portfolio))
                .mark_line()
                .encode(x="date", y="drawdown")
                .properties(width=700)
            )

            st.write(monthly_return_chart)
