import pandas as pd
import ta


class ATR:
    """Average True Range (ATR) volatility indicator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with DataFrame containing High, Low, Close.
        """
        required = {"High", "Low", "Close"}
        if not required.issubset(df.columns):
            raise ValueError("DataFrame must contain High, Low, Close columns.")

        self.df = df.copy()

    def calculate(self):
        """
        Add ATR_14 column to the DataFrame.
        """
        try:
            self.df["ATR_14"] = ta.volatility.average_true_range(
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                window=14
            )
        except Exception as e:
            raise RuntimeError(f"Failed to calculate ATR: {e}")

        return self.df
