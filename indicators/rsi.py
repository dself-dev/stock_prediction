import pandas as pd
from ta.momentum import RSIIndicator

class RSI:
    def __init__(self, df, window=14):
        """
        Initialize with a DataFrame and RSI window size.
        """
        self.df = df.copy()
        self.window = window

    def calculate(self):
        """
        Validate data, compute RSI, and return a DataFrame
        containing only the RSI_14 column.
        """
        try:
            # Ensure Close column exists
            if "Close" not in self.df.columns:
                raise KeyError("'Close' column not found in DataFrame.")

            # Convert Close to numeric
            self.df["Close"] = pd.to_numeric(self.df["Close"], errors="coerce")

            # Drop invalid or missing Close values
            self.df = self.df.dropna(subset=["Close"])

            if self.df.empty:
                raise ValueError("No valid 'Close' values available after cleaning.")

            # Compute RSI
            rsi_calc = RSIIndicator(close=self.df["Close"], window=self.window)
            self.df["RSI_14"] = rsi_calc.rsi()

            # Return only the RSI column
            return self.df[["RSI_14"]].copy()

        except Exception as e:
            raise RuntimeError(f"RSI calculation failed: {e}")
