import pandas as pd
import ta


class ATR:
    """Average True Range (ATR) volatility indicator."""

    WINDOW = 14

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
        Handles short datasets by filling with NaN.
        """

        # -----------------------------------------------------
        # FIX: Convert string values to numeric floats
        # -----------------------------------------------------
        for col in ["High", "Low", "Close"]:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # If not enough rows, return a full-length NaN column
        if len(self.df) < self.WINDOW:
            self.df["ATR_14"] = [float("nan")] * len(self.df)
            return self.df

        # Normal ATR calculation
        self.df["ATR_14"] = ta.volatility.average_true_range(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            window=self.WINDOW
        )

        return self.df
