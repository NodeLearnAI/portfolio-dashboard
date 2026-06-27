# components.py  ← new file in Module5/
import datetime
import streamlit as st
from data_loader import get_available_tickers

def render_sidebar():
    st.sidebar.title("Controls")
    tickers = get_available_tickers()
    
    # 1. Use the 'key' argument to automatically bind value to st.session_state["selected_ticker"]
    st.sidebar.selectbox(
        "Select Ticker",
        options=tickers,
        index=0,
        key="selected_ticker"
    )

    benchmarks = ['SPY', 'QQQ']
    # 2. Corrected copy-paste label typo from "Select Ticker" to "Select Benchmark"
    st.sidebar.selectbox(
        "Select Benchmark", 
        options=benchmarks,
        key="selected_benchmark"
    )

    # 3. Use standard datetime.date instead of pd.Timestamp to avoid unnecessary pandas import
    st.sidebar.date_input(
        "Start date", 
        value=datetime.date(2025, 1, 1),
        key="start_date"
    )
    st.sidebar.date_input(
        "End date", 
        value=datetime.date.today(),
        key="end_date"
    )
    
    # 4. Return the button click state so caller can use it directly if needed
    return st.sidebar.button("Analyse")