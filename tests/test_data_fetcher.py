import pytest
import pandas as pd
from unittest.mock import patch, MagicMock

# Fix for import path: Add project root so we can find services/
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.data_fetcher import DataFetcher  # Points to services/ folder

@pytest.fixture
def mock_yf_download():
    """
    Mock yfinance download so we don't hit real API in tests.
    Returns a fake DF with OHLCV columns.
    """
    mock_df = pd.DataFrame({
        'Open': [100.0],
        'High': [110.0],
        'Low': [90.0],
        'Close': [105.0],
        'Volume': [1000],
    }, index=pd.date_range(start='2024-01-01', periods=1))
    with patch('yfinance.download') as mock_download:
        mock_download.return_value = mock_df
        yield mock_download

def test_fetch_default_period(mock_yf_download):
    """
    Test fetching with default 5y period.
    Should call yf.download with period='5y' and return non-empty DF.
    """
    fetcher = DataFetcher()
    df = fetcher.fetch('AAPL')
    
    assert not df.empty
    assert list(df.columns) == ['Open', 'High', 'Low', 'Close', 'Volume']
    mock_yf_download.assert_called_once_with(
        'AAPL',
        period='5y',
        interval='1d',
        auto_adjust=False,
        progress=False
    )

def test_fetch_with_dates(mock_yf_download):
    """
    Test fetching with custom start/end dates.
    Should call yf.download with start/end instead of period.
    """
    fetcher = DataFetcher()
    df = fetcher.fetch('AAPL', start_date='2024-01-01', end_date='2024-12-31')
    
    assert not df.empty
    mock_yf_download.assert_called_once_with(
        'AAPL',
        start='2024-01-01',
        end='2024-12-31',
        interval='1d',
        auto_adjust=False,
        progress=False
    )

def test_fetch_invalid_ticker():
    """
    Test error for invalid ticker (empty string).
    """
    fetcher = DataFetcher()
    with pytest.raises(ValueError, match="Ticker must be a non-empty string."):
        fetcher.fetch('')

def test_fetch_no_data(mock_yf_download):
    """
    Test error when yf.download returns empty DF.
    """
    mock_yf_download.return_value = pd.DataFrame()  # Empty DF
    fetcher = DataFetcher()
    with pytest.raises(ValueError, match="No data returned for ticker: AAPL"):
        fetcher.fetch('AAPL')