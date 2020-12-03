import streamlit as st

st.sidebar.title('Aurora')

appOptions = ["Home","Backtest"]

currentPage = st.sidebar.radio("", appOptions)

mappingOptions = [
    {
        "appOptions": "Home",
        "title": "Aurora"
    }
]