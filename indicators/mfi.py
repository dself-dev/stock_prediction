import pandas as pd
import ta


class MFI:
    """Money Flow Index (MFI) indicator."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with a DataFrame containing High, Low, Close, and Volume.
        """
        required = {"High", "Low", "Close", "Volume"}
        if not required.issubset(df.columns):
            raise ValueError("DataFrame must contain High, Low, Close, and Volume columns.")

        self.df = df.copy()

    def calculate(self):
        """
        Add MFI_14 column to the DataFrame.
        """
        try:
            self.df["MFI_14"] = ta.volume.money_flow_index(
                high=self.df["High"],
                low=self.df["Low"],
                close=self.df["Close"],
                volume=self.df["Volume"],
                window=14
            )
        except Exception as e:
            raise RuntimeError(f"Failed to calculate Money Flow Index (MFI): {e}")

        return self.df
