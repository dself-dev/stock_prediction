import yfinance as yf
import pandas as pd

class DataFetcher:
    """
    Fetches raw market data from yfinance.
    I set this up to grab the data without messing with it yet.

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
        # Default settings for period, interval, and auto_adjust
        self.period = period
        self.interval = interval
        self.auto_adjust = auto_adjust

    def fetch(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        Download historical data for a ticker or crypto symbol.
        Now I added support for custom start/end dates from the user.
        If no dates are given, it falls back to the default period like 5y.
        """

        # Check if ticker is valid
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string.")

        # If dates are provided, use start/end for the download
        if start_date and end_date:
            df = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval=self.interval,
                auto_adjust=self.auto_adjust,
                progress=False,
            )
        # Otherwise, use the default period
        else:
            df = yf.download(
                ticker,
                period=self.period,
                interval=self.interval,
                auto_adjust=self.auto_adjust,
                progress=False,
            )

        # Make sure we got some data back
        if df is None or df.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        return df



# import yfinance as yf
# import pandas as pd


# class DataFetcher:
#     """
#     Fetches raw market data from yfinance.

#     Responsibilities:
#     - Accept a ticker or coin symbol (e.g., AAPL, BTC-USD)
#     - Download historical OHLCV data
#     - Return the raw DataFrame (unmodified)

#     This class does NOT:
#     - Clean data
#     - Rename columns
#     - Fix indexes
#     """

#     def __init__(
#         self,
#         period: str = "5y",
#         interval: str = "1d",
#         auto_adjust: bool = False,
#     ):
#         self.period = period
#         self.interval = interval
#         self.auto_adjust = auto_adjust

#     def fetch(self, ticker: str) -> pd.DataFrame:
#         """
#         Download historical data for a ticker or crypto symbol.
#         """

#         if not ticker or not isinstance(ticker, str):
#             raise ValueError("Ticker must be a non-empty string.")

#         df = yf.download(
#             ticker,
#             period=self.period,
#             interval=self.interval,
#             auto_adjust=self.auto_adjust,
#             progress=False,
#         )

#         if df is None or df.empty:
#             raise ValueError(f"No data returned for ticker: {ticker}")

#         return df
