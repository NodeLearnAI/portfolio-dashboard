#Also import files from /unit1.1
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import render_sidebar
import streamlit as st
from data_loader import get_available_tickers, get_ticker_data
from chart_builder import build_price_chart

render_sidebar()

ticker = st.session_state.get("selected_ticker", "META")
benchmark = st.session_state.get('selected_benchmark', "SPY")
start_date = st.session_state.get('start_date')
end_date = st.session_state.get('end_date')
st.title(f'Portfolio -- {ticker}')

df = get_ticker_data(ticker, start_date, end_date)
fig = build_price_chart(df, ticker, benchmark, start_date, end_date)
st.plotly_chart(fig, use_container_width=True)
