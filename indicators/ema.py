import pandas as pd
import ta


class EMA:
    """Exponential Moving Average calculator."""

    def __init__(self, df: pd.DataFrame):
        """
        I initialize with a DataFrame containing OHLC data.
        The DataFrame must contain a Close column.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")

        self.df = df.copy()

    def calculate(self):
        """
        I compute EMA_12 and EMA_26 and return the full DataFrame.
        I also convert Close to numeric in case the data came from a CSV.
        """

        # Convert Close to numeric if it came in as a string
        self.df["Close"] = pd.to_numeric(self.df["Close"], errors="coerce")

        # Standard EMA periods for MACD and general trend analysis
        self.df["EMA_12"] = ta.trend.ema_indicator(self.df["Close"], window=12)
        self.df["EMA_26"] = ta.trend.ema_indicator(self.df["Close"], window=26)

        return self.df
