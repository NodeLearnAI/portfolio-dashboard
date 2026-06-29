import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from metrics import (
    calculate_daily_returns,
    calculate_annualised_return,
    calculate_annualised_volatility,
    calculate_sharpe_ratio
)
from risk_metrics import calculate_max_drawdown

app = FastAPI(title="Portfolio API")

# What Is CORS?
# CORS stands for Cross-Origin Resource Sharing. It's a browser security rule.
# When your React frontend (running on localhost:3000) tries to call your FastAPI backend (running on localhost:8000), the browser sees two different origins — different port numbers count as different origins. By default the browser blocks this request for security reasons.
# CORS middleware tells your FastAPI server to include special headers in its responses that say "I allow requests from other origins." The browser sees those headers and permits the call.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"message": "Portfolio API is running"}

@app.get("/metrics/{ticker}")
def get_metrics(ticker: str, start: str, end: str):
    df = yf.download(ticker, start=start, end=end, auto_adjust=True)
    
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
    
    returns = calculate_daily_returns(df["Close"].squeeze())
    
    return {
        "ticker": ticker,
        "annualised_return": round(calculate_annualised_return(returns), 4),
        "annualised_volatility": round(calculate_annualised_volatility(returns), 4),
        "sharpe_ratio": round(calculate_sharpe_ratio(returns, 0.04), 4),
        "max_drawdown": round(calculate_max_drawdown(returns), 4)
    }