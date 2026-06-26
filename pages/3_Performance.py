import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from data_loader import get_ticker_data, get_available_tickers
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np
from metrics import (calculate_annualised_return, 
calculate_alpha_beta, 
calculate_daily_returns, 
calculate_cumulative_returns, 
calculate_annualised_volatility, 
calculate_sharpe_ratio, 
calculate_sortino_ratio)
from risk_metrics import (
    calculate_cvar,
    calculate_drawdown_series,
    calculate_max_drawdown,
    calculate_var
)


st.title("Performance Analytics")

available_tickers = get_available_tickers()

#-- SIDE BAR --
st.sidebar.header("Settings")
#Tickers
ticker = st.sidebar.text_input("Select Ticker", value = 'META')

benchmarks = ['SPY', 'QQQ']
benchmark = st.sidebar.selectbox("Select Ticker", options = benchmarks)

# Set Start/End Date
start     = st.sidebar.date_input("Start date", value=pd.Timestamp("2023-01-01"))
end       = st.sidebar.date_input("End date", value=pd.Timestamp.today())
# Analyse Btn
load_clicked = st.sidebar.button("Analyse")


if load_clicked:
    ticker_data = get_ticker_data(ticker, start, end)
    ticker_data['SMA_20'] = ticker_data['Close'].rolling(window = 20).mean()
    ticker_data['daily_returns'] = calculate_daily_returns(ticker_data['Close'])
    ticker_data['cumulative_return'] = (1 + ticker_data['daily_returns']).cumprod()
    risk_free_rate = 0.04
    colors = np.where(ticker_data['Close']>ticker_data['Open'], 'green', 'red')

    # Calculate benchmark returns
    benchmark_data = get_ticker_data(benchmark, start, end)
    benchmark_data['benchmark_returns'] = calculate_daily_returns(benchmark_data['Close'])
    
    #Display Metrics - annualised return, Sharpe ratio, max drawdown, and beta
    ann_return = calculate_annualised_return(ticker_data['daily_returns'])
    benchmark_ann_return = calculate_annualised_return(benchmark_data['benchmark_returns'])
    sharpe = calculate_sharpe_ratio(ticker_data['daily_returns'], risk_free_rate)
    max_drawdown = calculate_max_drawdown(ticker_data['daily_returns'])
    alpha, beta = calculate_alpha_beta(ticker_data['daily_returns'], benchmark_data['benchmark_returns'], risk_free_rate)

    col1, col2, col3, col4 = st.columns(4)
    
    delta_vs_spy = ann_return - benchmark_ann_return
    col1.metric("Ann. Return", f"{ann_return * 100:.2f}%", delta= f'{delta_vs_spy*100:.2f}% vs {benchmark}')
    col2.metric("Sharpe Ratio", f"{sharpe:.2f}")
    col3.metric("Max Drawdown", f"{max_drawdown * 100:.2f}%")
    col4.metric("Beta", f"{beta:.2f}")

    # Subplots - Price, Volume & Cumulative Returns
    fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.5, 0.25, 0.25]   # price panel gets 70% of the height, volume gets 30%
    )
    #Add price candlestick
    fig.add_trace(
    go.Candlestick(
        x=ticker_data["Date"], open=ticker_data["Open"], high=ticker_data["High"],
        low=ticker_data["Low"], close=ticker_data["Close"], name=ticker
    ),
    row=1, col=1
    )

    #Add bar chart to see volume
    fig.add_trace(
        go.Bar(
            x=ticker_data["Date"], y=ticker_data["Volume"],
            name="Volume",
            marker_color= colors,
            showlegend= False
        ),
        row=2, col=1
    )

    #Area chart to compare cumulative returns

# Cumulative return — fills to the baseline trace above
    # Invisible baseline at y=1.0
    fig.add_trace(go.Scatter(
    x=ticker_data["Date"],
    y=[1.0] * len(ticker_data),
    mode="lines",
    line=dict(color="rgba(0,0,0,0)"),  # transparent
    showlegend=False,
    hoverinfo="skip"
    ),
    row=3, col=1)

    fig.add_trace(go.Scatter(
    x=ticker_data["Date"],
    y=ticker_data["cumulative_return"],
    mode="lines",
    fill="tonexty",
    fillcolor="rgba(0, 180, 100, 0.2)",   # muted green fill
    line=dict(color="rgba(0, 180, 100, 0.9)"),
    name=ticker,
    showlegend=False
    ),
    row=3, col=1)
    
    #Draw a horizontal like at y=1
    fig.add_hline(y=1.0, line_dash="dash", line_color="gray", row=3, col=1)

    fig.update_layout(
    title=f"{ticker} Price & Volume",
    xaxis_rangeslider_visible=False,
    height=600
    )

    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative Returns", row=3, col=1)

    st.plotly_chart(fig, use_container_width=True)