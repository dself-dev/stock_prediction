# import pandas as pd
# from indicators.feature_builder import FeatureBuilder

# CSV_PATH = "test_csv/AAPL_2022-01-01_to_2025-10-27.csv"


# def test_feature_builder_runs_and_adds_columns():
#     # Load test data
#     df = pd.read_csv(CSV_PATH)

#     # Run FeatureBuilder
#     fb = FeatureBuilder(df)
#     out = fb.build()

#     # Basic checks
#     assert isinstance(out, pd.DataFrame)
#     assert len(out) == len(df)

#     # ---- Exact column names I am confident about ----
#     exact_columns = [
#         # ATR
#         "ATR_14",

#         # Bollinger
#         "Bollinger_Upper",
#         "Bollinger_Middle",
#         "Bollinger_Lower",

#         # MACD
#         "MACD",
#         "MACD_Signal",
#         "MACD_Histogram",

#         # MFI
#         "MFI",

#         # RSI
#         "RSI",
#     ]

#     for col in exact_columns:
#         assert col in out.columns, f"Missing column: {col}"

#     # ---- Looser checks for indicators where suffix/name may differ ----

#     # CCI: allow CCI, CCI_20, etc.
#     assert any(col.startswith("CCI") for col in out.columns), "No CCI column found"

#     # EMA: allow EMA, EMA_20, EMA_Close, etc.
#     assert any("EMA" in col for col in out.columns), "No EMA column found"

#     # SMA: allow SMA, SMA_20, SMA_14, etc.
#     assert any("SMA" in col for col in out.columns), "No SMA column found"

import pandas as pd
from indicators.feature_builder import FeatureBuilder

CSV_PATH = "test_csv/AAPL_2022-01-01_to_2025-10-27.csv"


def test_feature_builder_runs_and_adds_columns():
    # Load test data
    df = pd.read_csv(CSV_PATH)

    # Run FeatureBuilder
    fb = FeatureBuilder(df)
    out = fb.build()

    # Basic checks
    assert isinstance(out, pd.DataFrame)
    assert len(out) == len(df)

    # ---- Exact column names based on your REAL output ----
    exact_columns = [
        # ATR
        "ATR_14",

        # Bollinger
        "Bollinger_Upper",
        "Bollinger_Middle",
        "Bollinger_Lower",

        # MACD
        "MACD",
        "MACD_Signal",
        "MACD_Histogram",   # <-- your actual output

        # MFI
        "MFI_14",           # <-- your actual output

        # RSI
        "RSI_14",           # <-- your actual output
    ]

    for col in exact_columns:
        assert col in out.columns, f"Missing column: {col}"

    # ---- Looser checks for indicators where naming varies ----

    # CCI: allow CCI, CCI_20, etc.
    assert any(col.startswith("CCI") for col in out.columns), "No CCI column found"

    # EMA: allow any EMA-related column
    assert any("EMA" in col for col in out.columns), "No EMA column found"

    # SMA: allow any SMA-related column
    assert any("SMA" in col for col in out.columns), "No SMA column found"
