"""
Utility functions for Brent oil price analysis with type hints.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Union, Any, Optional

def validate_dataframe(df: Optional[pd.DataFrame], required_columns: List[str]) -> bool:
    """
    Validate dataframe has required columns.

    Args:
        df: pandas DataFrame to validate
        required_columns: list of required column names

    Returns:
        True if valid, False otherwise

    Example:
        >>> df = pd.DataFrame({'Date': ['2020-01-01'], 'Price': [50.0]})
        >>> validate_dataframe(df, ['Date', 'Price'])
        True
    """
    if df is None:
        return False
    
    if not isinstance(df, pd.DataFrame):
        return False

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"Missing columns: {missing}")
        return False

    return True

def calculate_log_returns(prices: Union[List[float], np.ndarray, pd.Series]) -> np.ndarray:
    """
    Calculate log returns from price series.

    Log returns are continuously compounded returns:
    r_t = ln(P_t) - ln(P_{t-1})

    Args:
        prices: array-like of price values

    Returns:
        numpy array of log returns (length = len(prices) - 1)

    Example:
        >>> prices = [100, 101, 102]
        >>> calculate_log_returns(prices)
        array([0.00995, 0.00985])
    """
    # Convert to numpy array if needed
    if isinstance(prices, pd.Series):
        prices = prices.values
    elif isinstance(prices, list):
        prices = np.array(prices)
    elif not isinstance(prices, np.ndarray):
        raise TypeError(f"Expected array-like, got {type(prices)}")
    
    # Check for negative prices (can't take log of negative)
    if np.any(prices <= 0):
        raise ValueError("Prices must be positive for log return calculation")
    
    # Calculate log returns
    log_prices = np.log(prices)
    returns = log_prices[1:] - log_prices[:-1]
    
    return returns

def date_to_index(date_series: pd.Series, target_date: datetime) -> int:
    """
    Convert date to index position in series.

    Args:
        date_series: pandas Series of datetime values
        target_date: datetime to find in the series

    Returns:
        index position if found, -1 if not found

    Example:
        >>> dates = pd.Series(pd.date_range('2020-01-01', periods=5))
        >>> date_to_index(dates, datetime(2020, 1, 3))
        2
    """
    try:
        # Ensure both are datetime
        if not isinstance(date_series.dtype, pd.DatetimeTZDtype):
            date_series = pd.to_datetime(date_series)
        
        # Find matching date
        mask = date_series == target_date
        if mask.any():
            return mask.idxmax()
        else:
            return -1
    except Exception as e:
        print(f"Error finding date: {e}")
        return -1

def calculate_rolling_volatility(
    returns: Union[List[float], np.ndarray], 
    window: int = 30
) -> np.ndarray:
    """
    Calculate rolling volatility (standard deviation) of returns.

    Args:
        returns: array of returns
        window: rolling window size in days

    Returns:
        numpy array of rolling volatility (same length as returns)
    """
    returns = np.array(returns)
    rolling_std = np.zeros_like(returns)
    
    for i in range(len(returns)):
        if i < window:
            rolling_std[i] = np.std(returns[:i+1])
        else:
            rolling_std[i] = np.std(returns[i-window+1:i+1])
    
    return rolling_std

def find_nearest_event(
    events_df: pd.DataFrame, 
    target_date: datetime,
    date_column: str = 'Date'
) -> pd.Series:
    """
    Find the event nearest to a target date.

    Args:
        events_df: DataFrame containing events with dates
        target_date: date to find nearest event to
        date_column: name of column containing dates

    Returns:
        Series containing the nearest event
    """
    # Calculate absolute difference in days
    events_df = events_df.copy()
    events_df['days_diff'] = abs((events_df[date_column] - target_date).dt.days)
    
    # Find minimum
    idx = events_df['days_diff'].idxmin()
    return events_df.loc[idx]

def format_business_impact(
    before_mean: float, 
    after_mean: float,
    change_date: datetime
) -> str:
    """
    Format business impact statement for reporting.

    Args:
        before_mean: average price before change
        after_mean: average price after change
        change_date: when the change occurred

    Returns:
        Formatted string describing business impact
    """
    pct_change = ((after_mean - before_mean) / before_mean) * 100
    abs_change = after_mean - before_mean
    
    impact = (
        f"**Business Impact:**\n"
        f"- Price regime shift detected on {change_date.strftime('%B %d, %Y')}\n"
        f"- Average price increased from ${before_mean:.2f} to ${after_mean:.2f}\n"
        f"- Absolute change: ${abs_change:.2f} per barrel\n"
        f"- Relative change: {pct_change:.1f}%\n"
    )
    
    if pct_change > 0:
        impact += "- This represents a significant increase in revenue potential"
    else:
        impact += "- This represents a significant decrease in revenue potential"
    
    return impact

# Version info
__version__ = "1.0.0"
__author__ = "Your Name"