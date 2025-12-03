'''NOTE: Indicator classes do NOT use try/except blocks internally.

This is intentional. Indicators act as a low-level computational layer, so errors must
bubble up naturally. Wrapping every calculation in try/except hides real failures and
makes debugging, testing, and API development harder. Higher-level layers (like the API
or UI) are responsible for catching errors and returning clean messages to the user.
Keeping indicators “pure” ensures professional, predictable behavior and makes pytest
and debugging far more accurate.
'''

import pandas as pd
from ta.momentum import RSIIndicator

class RSI:
    def __init__(self, df, window=14):
        """
        Initialize with a DataFrame and RSI window size.
        """
        if "Close" not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column.")

        self.df = df.copy()
        self.window = window

    def calculate(self):
        """
        Compute RSI and return the FULL DataFrame with a new RSI_14 column.
        """
        # Convert Close to numeric safely
        self.df["Close"] = pd.to_numeric(self.df["Close"], errors="coerce")

        # Compute RSI
        rsi_calc = RSIIndicator(close=self.df["Close"], window=self.window)
        self.df["RSI_14"] = rsi_calc.rsi()

        # RETURN FULL DATAFRAME — NOT ONLY RSI
        return self.df
