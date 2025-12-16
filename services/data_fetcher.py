import yfinance as yf
import pandas as pd


class DataFetcher:
    """
    Fetches raw market data from yfinance.

    Responsibilities:
    - Accept a ticker or coin symbol (e.g., AAPL, BTC-USD)
    - Download historical OHLCV data
    - Return the raw DataFrame (unmodified)

    This class does NOT:
    - Clean data
    - Rename columns
    - Fix indexes
    """

    def __init__(
        self,
        period: str = "5y",
        interval: str = "1d",
        auto_adjust: bool = False,
    ):
        self.period = period
        self.interval = interval
        self.auto_adjust = auto_adjust

    def fetch(self, ticker: str) -> pd.DataFrame:
        """
        Download historical data for a ticker or crypto symbol.
        """

        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string.")

        df = yf.download(
            ticker,
            period=self.period,
            interval=self.interval,
            auto_adjust=self.auto_adjust,
            progress=False,
        )

        if df is None or df.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        return df
