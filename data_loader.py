import yfinance as yf
import pandas as pd

def get_ticker_data(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)
    df = df.reset_index()
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]
    return df

def get_available_tickers() -> list:
    return ["GOOG", "AAPL", "MSFT", "META", "AMZN", "NVDA", "SPY"]