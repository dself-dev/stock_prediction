import pandas as pd
import ta


class CCI:
    """Commodity Channel Index (CCI) indicator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing High, Low, Close.
        """
        required = {"High", "Low", "Close"}
        if not required.issubset(df.columns):
            raise ValueError("DataFrame must contain High, Low, and Close columns.")

        self.df = df.copy()

    def calculate(self):
        """
        Add CCI_20 column to the DataFrame.
        """
        try:
            self.df["CCI_20"] = ta.trend.cci(
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                window=20
            )
        except Exception as e:
            raise RuntimeError(f"Failed to calculate CCI: {e}")

        return self.df
