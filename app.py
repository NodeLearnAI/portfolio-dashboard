import streamlit as st
from data_loader import get_available_tickers

st.set_page_config(page_title="Portfolio Dashboard", layout="wide")

# --- Sidebar ---
st.sidebar.title("Controls")

tickers = get_available_tickers()

selected_ticker = st.sidebar.selectbox(
    "Select Ticker",
    options=tickers,
    index=0
)

st.session_state["selected_ticker"] = selected_ticker

#Homepage content

st.title("Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Return", "—")
col2.metric("Annualised Return", "—")
col3.metric("Sharpe Ratio", "—")
col4.metric("Max Drawdown", "—")