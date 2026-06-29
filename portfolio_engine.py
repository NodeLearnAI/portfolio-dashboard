import pandas as pd
import yfinance as yf



def calculate_portfolio_returns(tickers, weights, start_date, end_date):
    # Step 1 — Fetch all price data
    # Step 2 — Extract Close prices into one DataFrame
    # Step 3 — Calculate daily returns for each ticker
    # Step 4 — Multiply by weights
    # Step 5 — Sum across columns → single portfolio return series

    #Step 1-3
    raw = yf.download(tickers, start_date, end_date)
    close_prices = raw['Close']
    daily_returns = close_prices.pct_change()

    #Step 4
    weights_series = pd.Series(weights)
    weighted_returns = daily_returns * weights_series

    #step 5
    portfolio_returns = weighted_returns.sum(axis = 1) #axis =1 means "sum across columns"

    return portfolio_returns

    

