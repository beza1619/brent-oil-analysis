"""
Unit tests for utility functions in src.utils
Run with: pytest tests/ -v
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# Add src to path so we can import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils import (
    validate_dataframe,
    calculate_log_returns,
    date_to_index,
    calculate_rolling_volatility,
    find_nearest_event,
    format_business_impact
)

# ==================== FIXTURES ====================

@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing."""
    return pd.DataFrame({
        'Date': pd.date_range('2020-01-01', periods=10),
        'Price': [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        'Volume': [1000] * 10
    })

@pytest.fixture
def sample_prices():
    """Create sample price array for testing."""
    return [100, 101, 102, 103, 104, 105]

@pytest.fixture
def sample_events():
    """Create sample events dataframe for testing."""
    return pd.DataFrame({
        'Event': ['Event A', 'Event B', 'Event C'],
        'Date': pd.to_datetime(['2020-01-15', '2020-06-15', '2020-12-15']),
        'Type': ['Economic', 'Geopolitical', 'Economic']
    })

# ==================== TEST VALIDATE DATAFRAME ====================

def test_validate_dataframe_valid(sample_dataframe):
    """Test that valid dataframe passes validation."""
    result = validate_dataframe(sample_dataframe, ['Date', 'Price'])
    assert result is True

def test_validate_dataframe_missing_columns(sample_dataframe):
    """Test that missing columns fail validation."""
    result = validate_dataframe(sample_dataframe, ['Date', 'Price', 'InvalidColumn'])
    assert result is False

def test_validate_dataframe_none():
    """Test that None fails validation."""
    result = validate_dataframe(None, ['Date', 'Price'])
    assert result is False

def test_validate_dataframe_empty_columns(sample_dataframe):
    """Test that empty required columns list passes."""
    result = validate_dataframe(sample_dataframe, [])
    assert result is True

def test_validate_dataframe_not_dataframe():
    """Test that non-dataframe input fails."""
    result = validate_dataframe("not a dataframe", ['Date'])
    assert result is False

# ==================== TEST CALCULATE LOG RETURNS ====================

def test_calculate_log_returns_basic():
    """Test basic log return calculation."""
    prices = [100, 110, 121]
    returns = calculate_log_returns(prices)
    
    # Expected: ln(110/100) ≈ 0.0953, ln(121/110) ≈ 0.0953
    expected = np.array([0.095310, 0.095310])
    np.testing.assert_array_almost_equal(returns, expected, decimal=5)

def test_calculate_log_returns_pandas_series():
    """Test with pandas Series input."""
    prices = pd.Series([100, 105, 110])
    returns = calculate_log_returns(prices)
    assert len(returns) == 2
    assert returns[0] > 0

def test_calculate_log_returns_numpy_array():
    """Test with numpy array input."""
    prices = np.array([100, 200, 300])
    returns = calculate_log_returns(prices)
    assert len(returns) == 2

def test_calculate_log_returns_empty():
    """Test with empty array."""
    with pytest.raises(ValueError):
        calculate_log_returns([])

def test_calculate_log_returns_negative_prices():
    """Test that negative prices raise error."""
    with pytest.raises(ValueError, match="Prices must be positive"):
        calculate_log_returns([-100, 100])

def test_calculate_log_returns_zero_prices():
    """Test that zero prices raise error."""
    with pytest.raises(ValueError, match="Prices must be positive"):
        calculate_log_returns([0, 100])

def test_calculate_log_returns_invalid_type():
    """Test with invalid input type."""
    with pytest.raises(TypeError):
        calculate_log_returns("not an array")

# ==================== TEST DATE TO INDEX ====================

def test_date_to_index_found():
    """Test finding existing date."""
    dates = pd.Series(pd.date_range('2020-01-01', periods=5))
    target = datetime(2020, 1, 3)
    result = date_to_index(dates, target)
    assert result == 2  # 0-based index

def test_date_to_index_not_found():
    """Test with date not in series."""
    dates = pd.Series(pd.date_range('2020-01-01', periods=5))
    target = datetime(2020, 2, 1)
    result = date_to_index(dates, target)
    assert result == -1

def test_date_to_index_empty_series():
    """Test with empty series."""
    dates = pd.Series([])
    target = datetime(2020, 1, 1)
    result = date_to_index(dates, target)
    assert result == -1

def test_date_to_index_string_dates():
    """Test with string dates."""
    dates = pd.Series(['2020-01-01', '2020-01-02', '2020-01-03'])
    target = datetime(2020, 1, 2)
    result = date_to_index(dates, target)
    assert result == 1

# ==================== TEST ROLLING VOLATILITY ====================

def test_calculate_rolling_volatility_basic():
    """Test basic rolling volatility calculation."""
    returns = [0.01, 0.02, -0.01, 0.01, -0.02]
    volatility = calculate_rolling_volatility(returns, window=3)
    
    assert len(volatility) == len(returns)
    assert volatility[0] >= 0  # First value should be non-negative

def test_calculate_rolling_volatility_window_larger():
    """Test with window larger than data."""
    returns = [0.01, 0.02, 0.01]
    volatility = calculate_rolling_volatility(returns, window=10)
    assert len(volatility) == 3

def test_calculate_rolling_volatility_constant_returns():
    """Test with constant returns (should have zero volatility)."""
    returns = [0.01] * 10
    volatility = calculate_rolling_volatility(returns, window=5)
    np.testing.assert_array_almost_equal(volatility, np.zeros(10))

# ==================== TEST FIND NEAREST EVENT ====================

def test_find_nearest_event(sample_events):
    """Test finding nearest event."""
    target = datetime(2020, 3, 1)
    nearest = find_nearest_event(sample_events, target)
    
    assert nearest['Event'] == 'Event A'  # Closest to Jan 15

def test_find_nearest_event_exact_match(sample_events):
    """Test with exact date match."""
    target = datetime(2020, 6, 15)
    nearest = find_nearest_event(sample_events, target)
    
    assert nearest['Event'] == 'Event B'

def test_find_nearest_event_empty():
    """Test with empty dataframe."""
    empty_df = pd.DataFrame(columns=['Event', 'Date', 'Type'])
    with pytest.raises(ValueError):
        find_nearest_event(empty_df, datetime(2020, 1, 1))

# ==================== TEST FORMAT BUSINESS IMPACT ====================

def test_format_business_impact_positive():
    """Test formatting with positive change."""
    change_date = datetime(2021, 6, 2)
    result = format_business_impact(50.0, 100.0, change_date)
    
    assert "Business Impact" in result
    assert "increased" in result
    assert "100.0%" in result or "100.0" in result
    assert "June 02, 2021" in result or "June 2, 2021" in result

def test_format_business_impact_negative():
    """Test formatting with negative change."""
    change_date = datetime(2020, 3, 1)
    result = format_business_impact(100.0, 50.0, change_date)
    
    assert "Business Impact" in result
    assert "decreased" in result
    assert "-50.0%" in result or "50.0%" in result

def test_format_business_impact_zero_change():
    """Test with zero change."""
    change_date = datetime(2021, 1, 1)
    result = format_business_impact(75.0, 75.0, change_date)
    
    assert "Business Impact" in result
    assert "0.0%" in result

# ==================== TEST EDGE CASES ====================

def test_calculate_log_returns_single_value():
    """Test with single price value."""
    with pytest.raises(ValueError):
        calculate_log_returns([100])

def test_validate_dataframe_with_duplicates():
    """Test validation with duplicate columns."""
    df = pd.DataFrame({'A': [1, 2], 'A': [3, 4]})  # Duplicate column
    result = validate_dataframe(df, ['A'])
    assert result is True  # Should still validate if column exists

def test_date_to_index_with_timezone():
    """Test with timezone-aware dates."""
    dates = pd.Series(pd.date_range('2020-01-01', periods=5, tz='UTC'))
    target = datetime(2020, 1, 3)
    result = date_to_index(dates, target)
    assert result == 2

# ==================== RUN TESTS ====================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])