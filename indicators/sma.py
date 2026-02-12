# import pandas as pd
# import ta


# class SMA:
#     """Simple Moving Average calculator."""

#     def __init__(self, df: pd.DataFrame):
#         """
#         Initialize with a DataFrame containing OHLCV data.
#         """
#         if "Close" not in df.columns:
#             raise ValueError("DataFrame must contain 'Close' column.")

#         self.df = df.copy()

#     def calculate(self):
#         """
#         Add SMA columns to the DataFrame.
#         """
#         try:
#             self.df["SMA_10"] = ta.trend.sma_indicator(self.df["Close"], window=10)
#             self.df["SMA_20"] = ta.trend.sma_indicator(self.df["Close"], window=20)
#             self.df["SMA_50"] = ta.trend.sma_indicator(self.df["Close"], window=50)

#         except Exception as e:
#             raise RuntimeError(f"Failed to calculate SMA: {e}")

#         return self.df
import pandas as pd
import ta


class SMA:
    """
    Simple Moving Average indicator
    Adds fixed-period SMAs: SMA_10, SMA_20, SMA_50
    """

    def __init__(self, df: pd.DataFrame):
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain a 'Close' column.")

        # Always work on a copy so we never mutate the original
        self.df = df.copy()

    def calculate(self) -> pd.DataFrame:
        """
        Calculates SMA_10, SMA_20, and SMA_50 and adds them to the DataFrame.

        Returns
        -------
        pd.DataFrame
            Original DataFrame with three new columns: SMA_10, SMA_20, SMA_50
        """
        close = self.df["Close"]

        self.df["SMA_10"] = ta.trend.sma_indicator(close, window=10)
        self.df["SMA_20"] = ta.trend.sma_indicator(close, window=20)
        self.df["SMA_50"] = ta.trend.sma_indicator(close, window=50)

        return self.df