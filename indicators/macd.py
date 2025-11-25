import pandas as pd
import ta


class MACD:
    """MACD (Moving Average Convergence Divergence) indicator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing OHLCV data.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")

        self.df = df.copy()

    def calculate(self):
        """
        Add MACD, Signal, and Histogram values to the DataFrame.
        """
        try:
            self.df["MACD"] = ta.trend.macd(self.df["Close"])
            self.df["MACD_Signal"] = ta.trend.macd_signal(self.df["Close"])
            self.df["MACD_Histogram"] = ta.trend.macd_diff(self.df["Close"])

        except Exception as e:
            raise RuntimeError(f"Failed to calculate MACD: {e}")

        return self.df
