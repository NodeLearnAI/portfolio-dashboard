#print the annualised return, print the annualised volatility, divide them yourself. 
from data_loader import get_ticker_data, get_multiple_tickers_data
from risk_metrics import calculate_var, calculate_drawdown_series
from correlation import calculate_correlation_matrix, calculate_portfolio_volatility
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

tickers = ['META', "SPY", "GLD", "GOOG"]

now = datetime.now()
start_date = (now - timedelta(days=365)).strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')

prices_wide = get_multiple_tickers_data(tickers, start_date, end_date).set_index('Date')
daily_returns = prices_wide.pct_change().dropna()

weights = [0.2, 0.2, 0.2, 0.2]
daily_cov_maxtrix = daily_returns.cov() * 252
portfolio_volatility = calculate_portfolio_volatility(weights, daily_cov_maxtrix)

#simple average
vol = daily_returns.std()
avg_vol = vol.mean() * np.sqrt(252)
print(f'Avg Vol: {avg_vol}')
print(f'Portfolio Vol: {portfolio_volatility}')
