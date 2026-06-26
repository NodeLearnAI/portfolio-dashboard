import pandas as pd
import numpy as np
import yfinance as yf


def calculate_correlation_matrix(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the pairwise correlation matrix of daily returns
    for all tickers in the given wide-format price DataFrame.

    Parameters
    ----------
    prices_df_META : wide-format DataFrame with Date as index and
                one column per ticker containing closing prices.
                (This is the output format of get_multiple_tickers())

    Returns
    -------
    Symmetric correlation matrix, tickers as both index and columns.
    All diagonal values are 1.0.
    """
    # Convert prices to daily returns first —
    # correlating raw prices is misleading because two stocks can both
    # trend upward over time and show high "correlation" simply because
    # they share a common trend, not because they actually move together day-to-day
    daily_returns = prices_df.pct_change().dropna()

    return daily_returns.corr()



def calculate_rolling_correlation(
    returns_a: pd.Series,
    returns_b: pd.Series,
    window: int = 60
) -> pd.Series:
    """
    Computes the rolling correlation between two return series
    over a sliding window of `window` trading days.

    This is more informative than a single static correlation number
    because correlations between assets change over time — especially
    during market stress when correlations tend to spike toward +1.

    Parameters
    ----------
    returns_a : daily returns for asset A
    returns_b : daily returns for asset B
    window    : rolling window in trading days (default 60 = ~3 months)

    Returns
    -------
    Series of rolling correlations, indexed by date.
    First (window - 1) values will be NaN.
    """
    aligned = pd.concat([returns_a, returns_b], axis=1).dropna()
    aligned.columns = ["a", "b"]

    return aligned["a"].rolling(window).corr(aligned["b"])


def calculate_portfolio_volatility(
    weights: np.ndarray,
    cov_matrix: pd.DataFrame
) -> float:
    """
    Computes annualised portfolio volatility using the full
    covariance matrix — the correct multi-asset generalisation
    of the two-asset formula you've seen in the theory.

    Parameters
    ----------
    weights    : array of portfolio weights (must sum to 1.0)
    cov_matrix : annualised covariance matrix of asset returns

    Returns
    -------
    Annualised portfolio volatility as a float.
    """
    # Matrix multiplication: w^T · Σ · w
    # This is the N-asset generalisation of the two-asset formula.
    # numpy's @ operator performs matrix multiplication.
    portfolio_variance = weights @ cov_matrix.values @ weights
    return np.sqrt(portfolio_variance)