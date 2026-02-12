import pandas as pd
import ta


class MACD:
    """MACD (Moving Average Convergence Divergence) indicator."""

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
        I compute MACD, MACD_Signal, and MACD_Histogram values
        and return the full DataFrame.
        I also convert Close to numeric in case the data came from a CSV.
        """

        # Convert Close to numeric if it came in as a string
        self.df["Close"] = pd.to_numeric(self.df["Close"], errors="coerce")

        # Standard MACD calculations using TA library
        self.df["MACD"] = ta.trend.macd(self.df["Close"])
        self.df["MACD_Signal"] = ta.trend.macd_signal(self.df["Close"])
        self.df["MACD_Histogram"] = ta.trend.macd_diff(self.df["Close"])

        return self.df
