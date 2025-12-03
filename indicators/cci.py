import pandas as pd
import ta


class CCI:
    """Commodity Channel Index (CCI) indicator."""

    def __init__(self, df: pd.DataFrame, window=20):
        required = {"High", "Low", "Close"}
        if not required.issubset(df.columns):
            raise ValueError("DataFrame must contain High, Low, and Close columns.")

        self.df = df.copy()
        self.window = window

    def calculate(self):
        """
        Compute CCI and return the full DataFrame.
        """

        # Convert OHLC columns to numeric in case they came from a CSV
        for col in ["High", "Low", "Close"]:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # Compute CCI
        self.df["CCI_20"] = ta.trend.cci(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            window=self.window
        )

        return self.df
