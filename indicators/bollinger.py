# import ta
# import pandas as pd

# class BollingerBands:
#     """Bollinger Bands indicator"""

#     def __init__(self, df: pd.DataFrame, window=20, window_dev=2):
#         if "Close" not in df.columns:
#             raise ValueError("DataFrame must contain 'Close' column.")
#         self.df = df.copy()
#         self.window = window
#         self.window_dev = window_dev

#     def calculate(self):
#         self.df["Bollinger_Upper"] = ta.volatility.bollinger_hband(
#             self.df["Close"], window=self.window, window_dev=self.window_dev
#         )
#         self.df["Bollinger_Middle"] = ta.volatility.bollinger_mavg(
#             self.df["Close"], window=self.window
#         )
#         self.df["Bollinger_Lower"] = ta.volatility.bollinger_lband(
#             self.df["Close"], window=self.window, window_dev=self.window_dev
#         )
#         return self.df
import pandas as pd
import ta


class Bollinger:
    """
    Bollinger Bands indicator
    Adds three columns to the DataFrame:
        - Bollinger_Upper
        - Bollinger_Middle (simple moving average)
        - Bollinger_Lower
    """

    def __init__(self, df: pd.DataFrame, window: int = 20, window_dev: int = 2):
        """
        Parameters
        ----------
        df : pd.DataFrame
            Must contain at least a 'Close' column.
        window : int, default 20
            Look-back period for the moving average and standard deviation.
        window_dev : int, default 2
            Number of standard deviations for the upper/lower bands.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain a 'Close' column.")

        # Work on a copy so we never mutate the caller's DataFrame
        self.df = df.copy()
        self.window = window
        self.window_dev = window_dev

    def calculate(self) -> pd.DataFrame:
        """
        Calculates the Bollinger Bands and adds them to the DataFrame.

        Returns
        -------
        pd.DataFrame
            Original DataFrame with three new columns:
            Bollinger_Upper, Bollinger_Middle, Bollinger_Lower
        """
        close = self.df["Close"]

        self.df["Bollinger_Middle"] = ta.volatility.bollinger_mavg(
            close, window=self.window
        )
        self.df["Bollinger_Upper"] = ta.volatility.bollinger_hband(
            close, window=self.window, window_dev=self.window_dev
        )
        self.df["Bollinger_Lower"] = ta.volatility.bollinger_lband(
            close, window=self.window, window_dev=self.window_dev
        )

        return self.df