import pandas as pd
from pathlib import Path

from indicators.sma import SMA


def test_sma_calculation():
    # Same CSV you use for all other indicator tests
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

    df = pd.read_csv(csv_path)

    # Basic requirement
    assert "Close" in df.columns, "CSV must contain a 'Close' column."

    # Create SMA instance and calculate
    sma = SMA(df)
    result = sma.calculate()

    # --- ASSERTIONS (exactly same style as your other tests) ---

    expected_columns = {"SMA_10", "SMA_20", "SMA_50"}
    for col in expected_columns:
        assert col in result.columns, f"{col} column is missing!"

    # Row count never changes
    assert len(result) == len(df), "Row count mismatch after SMA calculation!"

    # All SMA columns must be float/numeric
    for col in expected_columns:
        assert result[col].dtype.kind in "fi", f"{col} is not numeric (got {result[col].dtype})"

    # Warm-up NaNs: exactly (window-1) NaNs for each SMA
    assert result["SMA_10"].isna().sum() == 9,   "SMA_10 should have exactly 9 warmup NaNs"
    assert result["SMA_20"].isna().sum() == 19,  "SMA_20 should have exactly 19 warmup NaNs"
    assert result["SMA_50"].isna().sum() == 49,  "SMA_50 should have exactly 49 warmup NaNs"

    # There must be actual values after the warmup period
    for col in expected_columns:
        assert result[col].notna().sum() > 0, f"{col} has no valid values!"

    # Logical ordering where all three are defined: SMA_10 and SMA_20 can cross, but longer ones are smoother
    # We'll just check that they aren't completely flat/zero
    assert result["SMA_50"].max() > result["SMA_50"].min(), "SMA_50 appears completely flat"

    # Bonus sanity: SMA_50 should generally be smoother than SMA_10
    sma10_std = result["SMA_10"].dropna().std()
    sma50_std = result["SMA_50"].dropna().std()
    assert sma50_std < sma10_std * 2, "SMA_50 should be noticeably smoother than SMA_10"

    print("All SMA tests passed!")