import pandas as pd
import ta


class SMA:
    """Simple Moving Average calculator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing OHLCV data.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")

        self.df = df.copy()

    def calculate(self):
        """
        Add SMA columns to the DataFrame.
        """
        try:
            self.df["SMA_10"] = ta.trend.sma_indicator(self.df["Close"], window=10)
            self.df["SMA_20"] = ta.trend.sma_indicator(self.df["Close"], window=20)
            self.df["SMA_50"] = ta.trend.sma_indicator(self.df["Close"], window=50)

        except Exception as e:
            raise RuntimeError(f"Failed to calculate SMA: {e}")

        return self.df
