import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import yfinance as yf
from components import render_sidebar
from portfolio_engine import calculate_portfolio_returns

from metrics import (
    calculate_annualised_return,
    calculate_annualised_volatility,
    calculate_sharpe_ratio
)

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
st.session_state['summary_df'] = summary_df

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

    #Build inputs for portfolio engine
    weights = dict(zip(summary_df['Ticker'], summary_df['Weight']))
    tickers = summary_df['Ticker'].tolist()

    #Calculate portfolio returns
    start_date = st.session_state.get('start_date')
    end_date = st.session_state.get('end_date')
    portfolio_returns = calculate_portfolio_returns(tickers, weights, start_date, end_date)

    #Store portfolio_returns in session_state for other pages to use
    st.session_state['portfolio_returns'] = portfolio_returns
    print(portfolio_returns)
    #Calculate portfolio metrics ann_return , volatility, sharpe
    ann_return = calculate_annualised_return(portfolio_returns)
    volatility = calculate_annualised_volatility(portfolio_returns)
    sharpe = calculate_sharpe_ratio(portfolio_returns, 0.04)

    print(ann_return)
    print(volatility)
    print(sharpe)

    col1, col2, col3 = st.columns(3)
    col1.metric("Portfolio Ann. Return", f"{ann_return*100:.2f}%")
    col2.metric("Annualised Volatility", f"{volatility*100:.2f}%")
    col3.metric("Sharpe Ratio", f"{sharpe:.2f}")
