import pandas as pd
import ta


class Stochastic:
    """Stochastic Oscillator (Stoch_K, Stoch_D)."""

    WINDOW = 14
    SMOOTH_K = 3
    SMOOTH_D = 3

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
        Add Stoch_K and Stoch_D columns to the DataFrame.
        Handles short datasets by filling with NaN.
        """

        # Convert to numeric (same pattern as ATR)
        for col in ["High", "Low", "Close"]:
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")

        # Not enough rows → return NaNs
        if len(self.df) < self.WINDOW:
            self.df["Stoch_K"] = [float("nan")] * len(self.df)
            self.df["Stoch_D"] = [float("nan")] * len(self.df)
            return self.df

        stoch = ta.momentum.StochasticOscillator(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            window=self.WINDOW,
            smooth_window=self.SMOOTH_K
        )

        self.df["Stoch_K"] = stoch.stoch()
        self.df["Stoch_D"] = stoch.stoch_signal()

        return self.df
