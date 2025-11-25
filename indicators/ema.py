import pandas as pd
import ta


class EMA:
    """Exponential Moving Average calculator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing OHLCV data.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")
        
        self.df = df.copy()

    def calculate(self):
        """
        Add EMA columns to the DataFrame.
        """
        try:
            # Standard EMA periods for MACD calculations
            self.df["EMA_12"] = ta.trend.ema_indicator(self.df["Close"], window=12)
            self.df["EMA_26"] = ta.trend.ema_indicator(self.df["Close"], window=26)

        except Exception as e:
            raise RuntimeError(f"Failed to calculate EMA: {e}")

        return self.df
