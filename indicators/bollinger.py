import pandas as pd
import ta


class Bollinger:
    """Bollinger Bands indicator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing OHLCV data.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")

        self.df = df.copy()

    def calculate(self):
        """
        Add Bollinger Upper, Middle, and Lower bands to the DataFrame.
        """
        try:
            # Bollinger Bands (20-period, 2 std dev)
            self.df["Bollinger_Upper"] = ta.volatility.bollinger_hband(
                self.df["Close"], window=20, window_dev=2
            )
            self.df["Bollinger_Middle"] = ta.volatility.bollinger_mavg(
                self.df["Close"], window=20
            )
            self.df["Bollinger_Lower"] = ta.volatility.bollinger_lband(
                self.df["Close"], window=20, window_dev=2
            )

        except Exception as e:
            raise RuntimeError(f"Failed to calculate Bollinger Bands: {e}")

        return self.df
