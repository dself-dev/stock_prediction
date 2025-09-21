
"""
Service layer for computing technical indicators using yfinance and your
existing indicator functions. This file exposes a single callable,
`compute_indicators`, which the FastAPI layer can import and call.

Nothing here should perform I/O with `input()`; parameters are passed by function
arguments so the API can control them.
"""

from __future__ import annotations

from typing import List, Dict, Any, TypedDict, Optional
import pandas as pd
import yfinance as yf

# Import your existing indicator functions and SaveData exactly as you use them
from indicators.indicators import (
    RSI,
    BollingerBands,
    EMA,
    SMA,
    MACD,
    Stochastic,
    ATR,
    VolumeSMA,
    SaveData,
)


class IndicatorRow(TypedDict, total=False):
    """
    A single row of the computed DataFrame, returned to clients for preview.
    Keys are flexible because indicator sets can add columns dynamically.
    """
    # Common OHLCV keys yfinance returns (others may be present too).
    Date: Any
    Open: float
    High: float
    Low: float
    Close: float
    Adj_Close: float  # sometimes present
    Volume: float


class IndicatorsResult(TypedDict):
    """Structured result returned by compute_indicators."""
    ticker: str
    interval: str
    rows: int
    preview_tail_5: List[IndicatorRow]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    yfinance can return multi-index columns so i will use this to normalize them to a flat
    index so downstream code is predictable.
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    return df


def compute_indicators(
    ticker: str,
    interval: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    period: Optional[str] = None,
) -> IndicatorsResult:
    """
    Download historical data with yfinance, compute your indicators, and save
    the resulting dataset using your existing SaveData() helper.

    Parameters
    ----------
    ticker : str
        Ticker symbol (e.g., "AAPL", "IONQ"). Will be upper-cased.
    interval : str
        yfinance interval string (e.g., "1d", "1h", "30m", "15m").
        For "1d" you MUST pass start & end. For anything else, pass period.
    start : Optional[str]
        Start date in "YYYY-MM-DD" when interval == "1d".
    end : Optional[str]
        End date in "YYYY-MM-DD" when interval == "1d".
    period : Optional[str]
        Lookback like "730d", "90d", "2y" for intraday intervals.

    Returns
    -------
    IndicatorsResult
        Metadata plus a 5-row tail preview for quick inspection.

    Raises
    ------
    ValueError
        If required parameters are missing or yfinance returns no data.
    """
    t = ticker.upper()
    iv = interval.lower()

    # Enforce the same input rules your script used
    if iv == "1d":
        if not start or not end:
            raise ValueError("For interval='1d' you must provide start and end (YYYY-MM-DD).")
        df = yf.download(t, start=start, end=end, interval=iv)
    else:
        if not period:
            raise ValueError("For intraday intervals you must provide period (e.g. '730d', '90d', '2y').")
        df = yf.download(t, period=period, interval=iv)

    if df is None or df.empty:
        raise ValueError("No data returned from yfinance for the given parameters.")

    # Reset index so Date is a column and normalize column names
    df = df.reset_index()
    df = _normalize_columns(df)

    # Compute your full indicator set (in-place)
    RSI(df)
    BollingerBands(df)
    EMA(df)
    SMA(df)
    MACD(df)
    Stochastic(df)
    ATR(df)
    VolumeSMA(df)

    # Persist using your existing function (keeps your current storage format/paths, ithink??)
    SaveData(df, t, iv)

    # Return a small preview to avoid shoving huge payloads over HTTP and get kick out or off
    preview: List[IndicatorRow] = df.tail(5).to_dict(orient="records") 

    return IndicatorsResult(
        ticker=t,
        interval=iv,
        rows=len(df),
        preview_tail_5=preview,
    )
