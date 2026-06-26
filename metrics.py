import pandas as pd
import numpy as np

TRADING_DAYS_PER_YEAR = 252


def calculate_daily_returns(prices: pd.Series) -> pd.Series:
    """
    Converts a series of prices into daily percentage returns.
    The first value is always NaN since there's no prior day to compare to.
    """
    return prices.pct_change()


def calculate_cumulative_returns(daily_returns: pd.Series) -> pd.Series:
    """
    Compounds daily returns into cumulative returns over time.
    Uses cumprod(), not cumsum() — this is the compounding fix
    you already learned in your Module 4 capstone.
    """
    return (1 + daily_returns).cumprod() - 1


def calculate_annualised_return(daily_returns: pd.Series) -> float:
    """
    Annualises the average daily return by compounding it
    over a full trading year (252 days).
    """
    clean = daily_returns.dropna()
    total_returns = (1 + clean).prod()
    days = len(clean)
    return total_returns ** (TRADING_DAYS_PER_YEAR/days) -1


def calculate_annualised_volatility(daily_returns: pd.Series) -> float:
    """
    Annualises daily volatility using the square-root-of-time rule.
    Volatility scales by sqrt(252), not 252, because variance
    (not std dev) is what adds linearly across independent days.
    """
    daily_std = daily_returns.std()
    return daily_std * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_sharpe_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Risk-adjusted return, penalising ALL volatility (upside and downside).

    risk_free_rate is expected as an ANNUAL rate (e.g. 0.04 for 4%).
    """
    annualised_return     = calculate_annualised_return(daily_returns)
    annualised_volatility = calculate_annualised_volatility(daily_returns)

    if annualised_volatility == 0:
        return np.nan   # avoid division by zero for a flat/no-volatility series

    return (annualised_return - risk_free_rate) / annualised_volatility


def calculate_sortino_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.0) -> float:
    """
    Risk-adjusted return, penalising ONLY downside volatility.
    Almost always >= Sharpe for the same series, since the
    denominator excludes positive return days entirely.
    """
    annualised_return = calculate_annualised_return(daily_returns)

    # Keep only the days where returns were negative
    downside_returns = daily_returns[daily_returns < 0]

    if len(downside_returns) == 0:
        return np.nan   # no downside days — ratio is undefined, not infinite

    downside_std = downside_returns.std()
    annualised_downside_vol = downside_std * np.sqrt(TRADING_DAYS_PER_YEAR)

    if annualised_downside_vol == 0:
        return np.nan

    return (annualised_return - risk_free_rate) / annualised_downside_vol


def calculate_alpha_beta(
    asset_returns: pd.Series,
    benchmark_returns: pd.Series,
    risk_free_rate: float = 0.0
) -> tuple[float, float]:
    """
    Calculates alpha and beta via linear regression of asset returns
    against benchmark returns.

    Returns
    -------
    (alpha, beta) as a tuple of floats. Alpha is annualised.
    """
    # Align both series on matching dates only — critical step.
    # If asset and benchmark have different date ranges or gaps,
    # this prevents misaligned regression.

    aligned = pd.concat([asset_returns, benchmark_returns], axis=1).dropna()
    aligned.columns = ["asset", "benchmark"]

    if len(aligned) < 2:
        return np.nan, np.nan

    beta, daily_intercept = np.polyfit(aligned["benchmark"], aligned["asset"], deg=1)

    benchmark_annual_return = calculate_annualised_return(aligned["benchmark"])
    expected_return = risk_free_rate + beta * (benchmark_annual_return - risk_free_rate)
    asset_annual_return = calculate_annualised_return(aligned["asset"])

    alpha = asset_annual_return - expected_return

    return alpha, beta