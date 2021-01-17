import streamlit as st
import pandas as pd
from datetime import datetime
import altair as alt

from api.funds import get_funds, factorRegression


def display_factorRegression():

    # Portfolio Backtesting

    st.title("Factor Regression")
    fund_list = pd.DataFrame(get_funds())

    st.sidebar.subheader("Regression inputs")

    start_date = st.sidebar.date_input(
        "Start Date", value=datetime(2010, 12, 31)
    ).strftime("%Y-%m-%d")
    end_date = st.sidebar.date_input("End Date", value=datetime(2020, 12, 31)).strftime(
        "%Y-%m-%d"
    )

    selected_funds = st.sidebar.multiselect(
        label="Fund selection",
        options=list(fund_list["Company"]),
        default=["Apple Inc."],
    )

    regression_factors = ["MktRF", "SMB", "HML", "RMW", "CMA"]

    selected_factors = st.sidebar.multiselect(
        label="Factor selection",
        options=regression_factors,
        default=["MktRF", "SMB", "HML"],
    )

    selected_fund_list = []

    for i in range(0, len(selected_funds)):
        selected_fund_list.append(
            fund_list[fund_list["Company"] == selected_funds[i]]["Code"].reset_index(
                drop=True
            )[0]
        )

    if len(selected_funds) & len(selected_factors):
        regression_input = {
            "startDate": start_date,
            "endDate": end_date,
            "funds": selected_fund_list,
            "regressionFactors": selected_factors,
        }

        st.write(regression_input)

        regression_response = factorRegression(regression_input)

        st.write(regression_response)
