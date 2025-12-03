import pandas as pd
from pathlib import Path

from indicators.bollinger import BollingerBands


def test_bollinger_calculation():
    # Point to your existing test CSV (same one you use for ATR/RSI)
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

    # Load the data
    df = pd.read_csv(csv_path)

    # Basic requirement check
    assert "Close" in df.columns, "CSV must contain a 'Close' column."

    # Create Bollinger Bands instance (default 20-period, 2-std)
    bb = BollingerBands(df, window=20, window_dev=2)

    # Run the calculation
    result = bb.calculate()

    # --- ASSERTIONS (exactly the same style as your ATR and RSI tests) ---

    # 1. All three expected columns must be present
    expected_columns = {"Bollinger_Upper", "Bollinger_Middle", "Bollinger_Lower"}
    for col in expected_columns:
        assert col in result.columns, f"{col} column is missing!"

    # 2. Row count must not change
    assert len(result) == len(df), "Row count changed after calculation!"

    # 3. All Bollinger columns must be numeric
    for col in expected_columns:
        assert result[col].dtype.kind in "fi", f"{col} is not numeric (got {result[col].dtype})"

    # 4. Warm-up period: first 19 rows should be NaN for a 20-period window
    assert result["Bollinger_Middle"].isna().sum() == 19, "Expected exactly 19 NaN warm-up values for 20-period BB"
    assert result["Bollinger_Upper"].isna().sum() == 19
    assert result["Bollinger_Lower"].isna().sum() == 19

    # 5. There must be at least some real values after warm-up
    assert result["Bollinger_Middle"].notna().any(), "All middle band values are NaN!"
    assert result["Bollinger_Upper"].notna().any()
    assert result["Bollinger_Lower"].notna().any()

    # 6. Logical relationship: Upper ≥ Middle ≥ Lower (where all are defined)
    valid_mask = result[["Bollinger_Upper", "Bollinger_Middle", "Bollinger_Lower"]].notna().all(axis=1)
    valid = result.loc[valid_mask]

    assert (valid["Bollinger_Upper"] >= valid["Bollinger_Middle"]).all(), "Upper band must be ≥ middle band"
    assert (valid["Bollinger_Middle"] >= valid["Bollinger_Lower"]).all(), "Middle band must be ≥ lower band"

    # Optional: sanity check that bands actually move and aren't flat zero
    assert result["Bollinger_Upper"].max() > result["Bollinger_Middle"].mean(), "Upper band seems too flat"
    assert result["Bollinger_Lower"].min() < result["Bollinger_Middle"].mean(), "Lower band seems too flat"

    print("All Bollinger Bands tests passed!")