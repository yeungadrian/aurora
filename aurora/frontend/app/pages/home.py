import streamlit as st
from app.api.funds import get_funds

def display_home():
    st.title('Aurora')