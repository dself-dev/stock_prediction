import pandas as pd
import ta


class MFI:
    """Money Flow Index (MFI) indicator."""

    def __init__(self, df: pd.DataFrame, window=14):
        """
        I initialize with a DataFrame containing High, Low, Close, and Volume.
        """
        required = {"High", "Low", "Close", "Volume"}
        if not required.issubset(df.columns):
            raise ValueError("DataFrame must contain High, Low, Close, and Volume columns.")

        self.df = df.copy()
        self.window = window

    def calculate(self):
        """
        I compute the MFI_14 column and return the full DataFrame.
        I also convert all OHLC + Volume values to numeric in case the CSV
        saved them as strings.
        """

        # Convert OHLC + Volume to numeric if they came in as strings
        for col in ["High", "Low", "Close", "Volume"]:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # Compute MFI
        self.df["MFI_14"] = ta.volume.money_flow_index(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            volume=self.df["Volume"],
            window=self.window
        )

        return self.df
