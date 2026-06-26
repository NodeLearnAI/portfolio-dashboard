import streamlit as st

st.set_page_config(page_title="Performance Analytics", layout="wide")
st.title("Performance Analytics")

#-- SIDE BAR --
st.sidebar.header("Navigation")

# import streamlit as st
# import pandas as pd
# from db_loader import get_ticker_data, get_multiple_tickers_data, get_available_tickers
# from correlation import (
#     calculate_correlation_matrix,
#     calculate_portfolio_volatility,
#     calculate_rolling_correlation
# )
# from metrics import (
#     calculate_daily_returns,
#     calculate_cumulative_returns,
#     calculate_sharpe_ratio,
#     calculate_sortino_ratio,
#     calculate_alpha_beta
# )
# from risk_metrics import (
#     calculate_drawdown_series,
#     calculate_max_drawdown,
#     calculate_var,
#     calculate_cvar
# )


# st.set_page_config(page_title="Performance Analytics", layout="wide")
# st.title("Performance Analytics")

# available_tickers = ['GOOG', 'GLD', 'SPY', 'NEE']

# #-- SIDE BAR --
# st.sidebar.header("Settings")
# #Tickers
# selected_tickers = st.sidebar.multiselect("Select Tickers", options = available_tickers)
# # Set Start/End Date
# start     = st.sidebar.date_input("Start date", value=pd.Timestamp("2023-01-01"))
# end       = st.sidebar.date_input("End date", value=pd.Timestamp.today())
# # Analyse Btn
# load_clicked = st.sidebar.button("Analyse")


# if load_clicked:
#     if not selected_tickers:
#         st.warning("Please select at least one ticker.")
#     else:
#         prices_wide = get_multiple_tickers_data(selected_tickers, str(start), str(end))
#         if prices_wide.empty:
#             st.error("No data found for the selected tickers.")
#         else:
#             prices_wide = prices_wide.set_index("Date")
            
#             if len(selected_tickers) >= 2:

#                 st.subheader("Correlation matrix")

#                 corr_matrix = calculate_correlation_matrix(prices_wide)

#                 # Style the DataFrame with a colour gradient —
#                 # Streamlit's .style.background_gradient() applies a heatmap
#                 # colour scale directly to the rendered table, no Plotly needed
#                 styled = corr_matrix.style.background_gradient(
#                     cmap="RdYlGn",    # red = low correlation, green = high
#                     vmin=-1,
#                     vmax=1
#                 ).format("{:.2f}")    # show 2 decimal places in each cell

#                 st.dataframe(styled, use_container_width=True)

#                 st.divider()

#                 # Rolling correlation between the first two selected tickers
#                 if len(selected_tickers) >= 2:
#                     st.subheader(f"Rolling 60-day correlation: {selected_tickers[0]} vs {selected_tickers[1]}")

#                     returns = prices_wide.pct_change().dropna()

#                     rolling_corr = calculate_rolling_correlation(
#                         returns[selected_tickers[0]],
#                         returns[selected_tickers[1]],
#                         window=60
#                     )

#                     st.line_chart(rolling_corr)

# st.sidebar.header("Settings")
# #Tickers
# selected_tickers = st.sidebar.text_input("Ticker", value="AAPL")
# #Benchmark
# benchmark = st.sidebar.text_input("Benchmark", value="SPY")
# #Risk Free Rate
# risk_free_rate = st.sidebar.number_input("Risk free rate", value = 4)
# risk_free_rate = risk_free_rate/100
# #Confidence Level
# confidence_level = st.sidebar.slider("Confidence Level", value = 95)
# confidence_level = confidence_level/100
# #Set Start/End Date
# start     = st.sidebar.date_input("Start date", value=pd.Timestamp("2023-01-01"))
# end       = st.sidebar.date_input("End date", value=pd.Timestamp.today())
# #Analyse Btn
# load_clicked = st.sidebar.button("Analyse")
# 
# if load_clicked:
    # asset_df     = get_ticker_data(ticker, str(start), str(end))
    # benchmark_df = get_ticker_data(benchmark, str(start), str(end))
    #
    # if asset_df.empty or benchmark_df.empty:
    #     st.error("No data found for one or both tickers.")
    #     st.stop()
    #
    # asset_returns     = calculate_daily_returns(asset_df.set_index("Date")["Close"])
    # benchmark_returns = calculate_daily_returns(benchmark_df.set_index("Date")["Close"])
    #
    # sharpe  = calculate_sharpe_ratio(asset_returns, risk_free_rate)
    # sortino = calculate_sortino_ratio(asset_returns)
    # alpha, beta = calculate_alpha_beta(asset_returns, benchmark_returns, risk_free_rate)
    #
    # col1, col2, col3, col4 = st.columns(4)
    # with col1:
    #     st.metric("Sharpe ratio", f"{sharpe:.2f}")
    # with col2:
    #     st.metric("Sortino ratio", f"{sortino:.2f}")
    # with col3:
    #     st.metric("Alpha (annual)", f"{alpha:.1%}")
    # with col4:
    #     st.metric("Beta", f"{beta:.2f}")
    #
    # 
    # max_dd = calculate_max_drawdown(asset_returns)
    # var_95 = calculate_var(asset_returns, confidence_level)
    # cvar_95 = calculate_cvar(asset_returns, confidence_level)
    #
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.metric("Max drawdown", f"{max_dd:.1%}")
    # with col2:
    #     st.metric("VaR (95%, 1-day)", f"{var_95:.2%}")
    # with col3:
    #     st.metric("CVaR (95%, 1-day)", f"{cvar_95:.2%}")
    #
    # st.divider()
    # st.subheader("Drawdown over time")
    #
    # drawdown_series = calculate_drawdown_series(asset_returns)
    # st.area_chart(drawdown_series)

    #st.divider()
    #st.subheader("Cumulative return vs benchmark")

    #cum_asset     = calculate_cumulative_returns(asset_returns)
    #cum_benchmark = calculate_cumulative_returns(benchmark_returns)

    #comparison_df = pd.DataFrame({
    #    ticker:    cum_asset,
    #    benchmark: cum_benchmark
    #})

    #st.line_chart(comparison_df)


# import streamlit as st
# import yfinance as yf
# import pandas as pd
# from db_loader import get_connection, get_available_tickers, get_ticker_data, get_multiple_tickers_data
#
# # st.set_page_config must be the very first Streamlit call in the script.
# # layout="wide" uses the full browser width instead of a narrow centered column.
# st.set_page_config(page_title="Stock Viewer", layout="wide")
#
# st.title("Stock Price Viewer")
# st.write("Enter a ticker and lookback period to see price history.")
#
#
# # @st.cache_data tells Streamlit: cache the return value of this function.
# # The cache key is the combination of (ticker, period).
# # TTL (time-to-live) = 3600 seconds = 1 hour. After 1 hour, the cache expires
# # and the next call will re-fetch fresh data from Yahoo Finance.
# @st.cache_data(ttl=3600)
# def load_prices(ticker, start_date, end_date):
#     return get_ticker_data(ticker, start_date, end_date)
#
# @st.cache_data(ttl=3600)
# def load_tickers():
#     return get_available_tickers()
# # --- SIDEBAR CONTROLS ---
# # st.sidebar.anything() puts the widget in the collapsible left panel.
# # This keeps the main area clean for charts and data.
#
# st.sidebar.header("Settings")
#
# tickers = get_available_tickers()
# selected_tickers = st.sidebar.multiselect(
#     label = "Ticker",
#     options = tickers
#
# )
#
# period = st.sidebar.selectbox(
#     label="Lookback period",
#     options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
#     index=3                # default to "1y" (index 3 in the list)
# )
#
# raw_data_checkbox = st.sidebar.checkbox(
#     label = "Show Raw Data",
#     value = True
# )
#
# start_date = st.sidebar.date_input("Start Date", value = pd.Timestamp("2023-01-01"))
# end_date = st.sidebar.date_input("End Date", value = pd.Timestamp.today())
# # st.sidebar.button returns True only on the run immediately after it's clicked,
# # then returns False again on the next rerun. It is not a toggle.
# load_clicked = st.sidebar.button("Load data")
#
#
#
# # --- MAIN LOGIC ---
# # We only load data when the button is clicked.
# # The 'if load_clicked' guard prevents the app from fetching data
# # on the very first load before the user has done anything.
#
# if load_clicked:
#     if not selected_tickers:
#         st.warning("Select at least one ticker before loading data.")
#         st.stop()
#
#     if len(selected_tickers) == 1:
#         ##-- Load Single Ticker --
#         # Show a spinner while the data loads (especially useful if cache is cold)
#         ticker = selected_tickers[0]
#         with st.spinner(f"Fetching {ticker} data..."):
#             df = load_prices(ticker, start_date, end_date)
#             df['SMA_20'] = df['Close'].rolling(window = 20).mean()
#
#         if df.empty:
#             # st.error renders a red alert box
#             st.error(f"No data found for ticker '{ticker}'. Check the symbol and try again.")
#         else:
#             # --- KPI METRICS ROW ---
#             # st.columns(3) splits the main area into 3 equal-width columns.
#             # We unpack them into col1, col2, col3.
#             col1, col2, col3 = st.columns(3)
#
#             latest_close = df["Close"].iloc[-1]
#             first_close  = df["Close"].iloc[0]
#             total_return = (latest_close / first_close - 1) * 100
#
#             with col1:
#                 # st.metric shows a labelled number with an optional delta.
#                 # delta_color="normal" = green for positive, red for negative.
#                 st.metric(
#                     label="Latest close",
#                     value=f"${latest_close:.2f}"
#                 )
#
#             with col2:
#                 st.metric(
#                     label=f"Total return ({period})",
#                     value=f"{total_return:.1f}%",
#                     delta=f"{total_return:.1f}%"
#                 )
#
#             with col3:
#                 st.metric(
#                     label="Data points",
#                     value=f"{len(df):,} days"
#                 )
#
#         # You can also use the following format to produce the column displays,
#             # but 'with' is preferred when you need to add multiple things into one column
#             # col1.metric(label="Latest close", value=f"${latest_close:.2f}")
#             # col2.metric(label=f"Total return ({period})", value=f"{total_return:.1f}%")
#             # col3.metric(label="Data points", value=f"{len(df):,} days")
#
#             st.divider()   # draws a horizontal rule
#
#             # --- PRICE CHART ---
#             st.subheader("Closing price")
#
#             # st.line_chart expects a DataFrame where the index is the x-axis
#             # and the columns become the lines. We set Date as index here.
#             st.line_chart(df.set_index("Date")[["Close","SMA_20"]])
#
#             st.divider()
#
#             # --- VOLUME CHART ---
#             st.subheader("Volume")
#
#             st.bar_chart(df.set_index("Date")["Volume"])
#
#             st.divider()
#
#             
#
#     else:
#
#         #-- Load Chart for muliple tickers' data --
#         with st.spinner(f'Fetching {', '.join(selected_tickers)} data'):
#             df = get_multiple_tickers_data(selected_tickers, start_date,end_date)
#
#         if df.empty:
#             st.warning("No data found for the selected tickers and date range.")
#         else:
#             st.subheader("Closing price")
#    
#
#            # Each remaining column is one ticker's closing price, so plotting
#            # the whole frame draws one line per ticker.
#            st.line_chart(df.set_index('Date'))
#
#     # --- RAW DATA TABLE ---
#             if raw_data_checkbox:
#                 st.subheader("Raw data")
#
#                 # st.dataframe renders an interactive table.
#                 # use_container_width=True makes it fill the column width.
#                 st.dataframe(df, use_container_width=True)