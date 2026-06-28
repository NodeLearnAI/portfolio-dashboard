import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import yfinance as yf
from components import render_sidebar

render_sidebar()
st.title("My Holdings")

# Initialise holdings in session state if it doesn't exist yet
if "holdings" not in st.session_state:
    st.session_state["holdings"] = pd.DataFrame(
        columns=["Ticker", "Shares", "Cost Basis"]
    )

# Editable holdings table
edited_df = st.data_editor(
    st.session_state["holdings"],
    num_rows="dynamic",
    use_container_width=True,
    key="holdings_editor"

)

#Get edited_df tickers' price
rows = []
for index, row in edited_df.iterrows():
    if pd.isna(row["Ticker"]) or pd.isna(row['Shares']):
        continue

    ticker = row['Ticker']
    shares = float(row["Shares"])
    cost = float(row['Cost Basis'])



    ticker = str(ticker).strip().upper()
    try:
        #fast_info is a lightweight call that returns just the metadata including last price.
        current_price = yf.Ticker(ticker).fast_info['last_price']
        market_value = current_price * shares
        profit_and_loss = (current_price - cost) * shares
        
        rows.append({
            "Ticker": ticker,
            "Shares": shares,
            "Cost Basis": cost,
            "Current Price": current_price,
            "Market Value": market_value,
            "Profit/Loss": profit_and_loss
        })
    except Exception as e:
        st.error(f"Error fetching data for ticker {ticker}: {e}")

summary_df = pd.DataFrame(rows)

if not summary_df.empty:
    total_market_value = summary_df['Market Value'].sum()
    summary_df['Weight'] = summary_df['Market Value']/total_market_value
  
    st.dataframe(summary_df.style.format({
        'Weight': '{:.2%}',
        'Shares': '{:.0f}',
        'Cost Basis': '${:.2f}',
        'Profit/Loss': '${:.2f}',
        'Market Value': '${:.2f}',
        'Current Price': '${:.2f}'
    }))
else:
    st.info("No holdings to display. Add rows with valid tickers and shares to the table above.")

# Save edits back to session state
if st.button("Analyse Portfolio"):
    st.session_state["holdings"] = edited_df