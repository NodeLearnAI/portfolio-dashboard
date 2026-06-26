import pandas as pd
import numpy as np


def calculate_drawdown_series(daily_returns: pd.Series) -> pd.Series:
    """
    Returns the full drawdown series — one value per day, showing
    how far below the running peak the asset currently sits.
    Values are <= 0 (0 means at a new all-time high).
    """
    cumulative = (1 + daily_returns).cumprod()
    running_peak = cumulative.cummax()
    drawdown = (cumulative - running_peak) / running_peak
    return drawdown


def calculate_max_drawdown(daily_returns: pd.Series) -> float:
    """
    Returns the single worst drawdown value over the whole period.
    A more negative number means a deeper fall (e.g. -0.45 = -45%).
    """
    drawdown_series = calculate_drawdown_series(daily_returns)
    return drawdown_series.min()


def calculate_var(daily_returns: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Historical Value-at-Risk. Returns the daily return threshold
    below which losses fall on (1 - confidence_level) of days.

    Example: confidence_level=0.95 returns the 5th percentile of returns.
    """
    return daily_returns.quantile(1 - confidence_level)


def calculate_cvar(daily_returns: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Conditional VaR / Expected Shortfall.
    Averages all returns that fall at or below the VaR threshold —
    answers "how bad does it get, on average, when it's already bad?"
    """
    var_threshold = calculate_var(daily_returns, confidence_level)
    tail_returns = daily_returns[daily_returns <= var_threshold]

    if tail_returns.empty:
        return np.nan

    return tail_returns.mean()