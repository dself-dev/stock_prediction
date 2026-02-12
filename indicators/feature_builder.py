import pandas as pd

from indicators.atr import ATR
from indicators.bollinger import Bollinger
from indicators.cci import CCI
from indicators.ema import EMA
from indicators.macd import MACD
from indicators.mfi import MFI
from indicators.rsi import RSI
from indicators.sma import SMA


class FeatureBuilder:
    """
    Takes a raw OHLCV DataFrame and adds ALL indicator columns
    by running each indicator class you created.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def build(self) -> pd.DataFrame:
        """
        Run all indicators in sequence and return the final DataFrame.
        """

        # ---- ATR ----
        self.df = ATR(self.df).calculate()

        # ---- Bollinger Bands ----
        self.df = Bollinger(self.df).calculate()

        # ---- CCI ----
        self.df = CCI(self.df).calculate()

        # ---- EMA ----
        self.df = EMA(self.df).calculate()

        # ---- MACD ----
        self.df = MACD(self.df).calculate()

        # ---- MFI ----
        self.df = MFI(self.df).calculate()

        # ---- RSI ----
        self.df = RSI(self.df).calculate()

        # ---- SMA ----
        self.df = SMA(self.df).calculate()

        return self.df
