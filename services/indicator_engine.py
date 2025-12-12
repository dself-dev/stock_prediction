# import pandas as pd

# from indicators.rsi import RSI
# from indicators.sma import SMA
# from indicators.ema import EMA
# from indicators.macd import MACD
# from indicators.bollinger import BollingerBands
# from indicators.atr import ATR
# from indicators.mfi import MFI
# from indicators.cci import CCI


# # ===========================================================
# # Indicator Registry
# # Maps short names → classes
# # ===========================================================
# INDICATOR_MAP = {
#     "rsi": RSI,
#     "sma": SMA,
#     "ema": EMA,
#     "macd": MACD,
#     "bollinger": BollingerBands,
#     "atr": ATR,
#     "mfi": MFI,
#     "cci": CCI
# }


# class IndicatorEngine:
#     """
#     Runs technical indicators on a DataFrame.

#     HOW IT WORKS:
#     -------------
#     - If indicators=None → runs ALL indicators (auto mode)
#     - If indicators=["rsi", "macd"] → runs ONLY those

#     This makes it perfect for:
#         • API requests
#         • predict_tomorrow.py
#         • User-selected indicators in UI
#         • ML model feature generation
#     """

#     def __init__(self, df: pd.DataFrame, indicators: list[str] = None):
#         if "Close" not in df.columns:
#             raise ValueError("DataFrame must contain a 'Close' column.")

#         self.df = df.copy()
#         self.indicators = indicators  # None = auto mode

#     def run(self) -> pd.DataFrame:
#         """
#         Apply selected indicators and return updated DataFrame.
#         """
#         # -----------------------------
#         # Auto Mode: run every indicator
#         # -----------------------------
#         if self.indicators is None:
#             selected_classes = INDICATOR_MAP.values()

#         else:
#             # -----------------------------
#             # Custom Mode: run only specific indicators ..the user can
#             # -----------------------------
#             selected_classes = []
#             for name in self.indicators:
#                 name = name.lower()
#                 if name not in INDICATOR_MAP:
#                     raise ValueError(f"Unknown indicator: '{name}'")
#                 selected_classes.append(INDICATOR_MAP[name])

#         # -----------------------------
#         # Run each indicator sequentially
#         # -----------------------------
#         for indicator_class in selected_classes:
#             self.df = indicator_class(self.df).calculate()

#         return self.df
# indicators/engine.py
# my central indicator engine – nothing fancy, just works
# i will throw every indicator in here over time

# from typing import List, Dict, Any
# import pandas as pd

# # empty dict where all indicators live
# INDICATOR_REGISTRY = {}

# def register(name: str):
#     """
#     decorator so i only have to write one line when i add a new indicator
#     usage: @register("rsi")
#     """
#     def wrapper(cls):
#         # this turns the class into a function that takes df -> runs .calculate()
#         def runner(df: pd.DataFrame):
#             return cls(df).calculate()
#         INDICATOR_REGISTRY[name.lower()] = runner
#         return cls
#     return wrapper

# # ————————————————————————
# # register the ones i actually have right now
# # ————————————————————————
# from indicators.rsi import RSI
# from indicators.bollinger import BollingerBands

# @register("rsi")
# class RSI(RSI): pass   # yeah i know it's dumb, just keeps the original class untouched

# @register("bollinger")
# class BollingerBands(BollingerBands): pass

# # later i’ll just copy-paste these lines:
# # @register("sma")        class SMA(SMA): pass
# # @register("atr")        class ATR(ATR): pass
# # @register("cci")        class CCI(CCI): pass


# def apply_indicators(
#     df: pd.DataFrame,
#     use: List[str] = None
# ) -> tuple[pd.DataFrame, dict]:
#     """
#     main function i will call everywhere
#     give it a df and a list like ["rsi","bollinger"] or nothing → runs everything
#     returns (full dataframe with all columns, dict of only the latest values)
#     """
#     if use is None or len(use) == 0:
#         selected = list(INDICATOR_REGISTRY.keys())
#     else:
#         selected = [x.lower() for x in use]

#     working_df = df.copy()

#     for indicator_name in selected:
#         if indicator_name not in INDICATOR_REGISTRY:
#             raise ValueError(f"no indicator called '{indicator_name}'. i have: {list(INDICATOR_REGISTRY.keys())}")

#         print(f"running {indicator_name}...")
#         working_df = INDICATOR_REGISTRY[indicator_name](working_df)

#     # build the dict with only the newest row – perfect for prediction later
#     last_row = working_df.iloc[-1]
#     original_columns = set(df.columns)

#     latest = {
#         "date": working_df.index[-1] if isinstance(working_df.index, pd.DatetimeIndex) else None,
#         "close": last_row.get("Close"),
#     }

#     # grab every column i just added
#     for col in working_df.columns:
#         if col not in original_columns:
#             latest[col.lower()] = last_row[col]   # lowercase keys because i like it that way

#     return working_df, latest


# indicators/engine.py
from typing import List, Dict, Any
import pandas as pd

# empty dict where all indicators live
INDICATOR_REGISTRY = {}

def register(name: str):
    """
    decorator so i only have to write one line when i add a new indicator
    usage: @register("rsi")
    """
    def wrapper(cls):
        # this turns the class into a function that takes df -> runs .calculate()
        def runner(df: pd.DataFrame):
            return cls(df).calculate()
        INDICATOR_REGISTRY[name.lower()] = runner
        return cls
    return wrapper


# ————————————————————————
# import the indicator classes
# ————————————————————————
from indicators.rsi import RSI
from indicators.bollinger import Bollinger
from indicators.atr import ATR
from indicators.cci import CCI


# ————————————————————————
# register the indicators
# ————————————————————————
@register("rsi")
class RSI(RSI): pass

@register("bollinger")
class Bollinger(Bollinger): pass

@register("atr")
class ATR(ATR): pass

@register("cci")
class CCI(CCI): pass


# ————————————————————————
# main apply function
# ————————————————————————
def apply_indicators(
    df: pd.DataFrame,
    use: List[str] = None
) -> tuple[pd.DataFrame, dict]:
    """
    give it a df and a list like ["rsi","bollinger","atr"] or nothing → runs everything
    returns (full dataframe with all columns, dict of only the latest values)
    """
    if use is None or len(use) == 0:
        selected = list(INDICATOR_REGISTRY.keys())
    else:
        selected = [x.lower() for x in use]

    working_df = df.copy()

    for indicator_name in selected:
        if indicator_name not in INDICATOR_REGISTRY:
            raise ValueError(f"no indicator called '{indicator_name}'. i have: {list(INDICATOR_REGISTRY.keys())}")

        print(f"running {indicator_name}...")
        working_df = INDICATOR_REGISTRY[indicator_name](working_df)

    # build the dict with only the newest row – perfect for prediction later
    last_row = working_df.iloc[-1]
    original_columns = set(df.columns)

    latest = {
        "date": working_df.index[-1] if isinstance(working_df.index, pd.DatetimeIndex) else None,
        "close": last_row.get("Close"),
    }

    # grab only the new indicator columns
    for col in working_df.columns:
        if col not in original_columns:
            latest[col.lower()] = last_row[col]

    return working_df, latest
