""" Exercise 3 — Use get_multiple_tickers. In app.py, swap the selectbox for a st.sidebar.multiselect 
widget (it lets users pick multiple options from a list). Pass the selected list to 
get_multiple_tickers and plot all closing prices on a single st.line_chart. This is the 
foundation of the portfolio comparison chart in your capstone.

Exercise 4 — Add a fallback. Modify get_ticker_data so that if the returned DataFrame is empty, 
it automatically falls back to fetching from yfinance using the same ticker and date range. 
This makes your app resilient — if a user types a ticker that isn't in the database yet, it 
still works. Hint: you already wrote yfinance fetch logic in Unit 1.1 """

import sqlite3
import pandas as pd
from pathlib import Path
import yfinance as yf
DB_PATH = Path(r'C:\DailyInvestmentBrief\Code\Python Practice\Module4') / 'data' / 'pipeline.db'

def get_connection():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found at {DB_PATH}. "
            f"Run your Module 4 pipeline first to populate it."
        )
    return sqlite3.connect(DB_PATH)

def get_available_tickers():
    conn = get_connection()
    query = "SELECT DISTINCT ticker FROM prices ORDER BY ticker"
    try:
        df = pd.read_sql_query(query, conn)
        return df['ticker'].tolist()
    
    finally:
        conn.close()

def get_ticker_data(ticker: str, start_date: str = None, end_date: str = None):
    
    df = yf.download(ticker, start_date, end_date)
    df.columns = [col[0] for col in df.columns]

    return df.reset_index()

    """ conn = get_connection()
    try:
        
        query = 'SELECT * FROM prices WHERE ticker = ?'
        params = [ticker]

        if start_date:
            query += ' AND date>= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND date<= ?'
            params.append(end_date)

        df = pd.read_sql_query(query, conn, params= params)
    finally:
        conn.close()

    df['date'] = pd.to_datetime(df['date'])

    df = df.rename(
        columns= {
            'date':"Date",
            "open":   "Open",
            "high":   "High",
            "low":    "Low",
            "close":  "Close",
            "volume": "Volume"
        }
    )

    # Prices/volume are stored as TEXT in the DB, so they come back as object
    # (string) dtype. Coerce to numeric so charts and rolling means work.
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df """
    

def get_multiple_tickers_data(tickers, start_date, end_date):
    frames = []
    for ticker in tickers:
        df = get_ticker_data(ticker, start_date, end_date)
    
        if df.empty:
            continue
        # Keep only Date + Close, and rename Close to the ticker symbol so
        # each ticker becomes its own column after merging.
        frame = df[["Date", "Close"]].rename(columns={"Close": ticker})
        frames.append(frame)

    if not frames:
        return pd.DataFrame()

    result = frames[0]
    for frame in frames[1:]:
        result = result.merge(frame, on="Date", how="outer")

    return result.sort_values("Date").reset_index(drop=True)
    
    
