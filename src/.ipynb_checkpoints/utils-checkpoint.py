"""
Utility functions for Brent oil price analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime

def validate_dataframe(df, required_columns):
    """
    Validate dataframe has required columns
    
    Parameters:
    df: pandas DataFrame
    required_columns: list of required column names
    
    Returns:
    bool: True if valid, False otherwise
    """
    if df is None:
        return False
    
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        print(f"Missing columns: {missing}")
        return False
    
    return True

def calculate_log_returns(prices):
    """
    Calculate log returns from price series
    
    Parameters:
    prices: array-like of prices
    
    Returns:
    numpy array of log returns
    """
    prices = np.array(prices)
    log_prices = np.log(prices)
    returns = log_prices[1:] - log_prices[:-1]
    return returns

def date_to_index(date_series, target_date):
    """
    Convert date to index position in series
    
    Parameters:
    date_series: pandas Series of datetime
    target_date: datetime to find
    
    Returns:
    int: index position, or -1 if not found
    """
    try:
        return (date_series == target_date).idxmax()
    except:
        return -1