import pandas as pd
from pathlib import Path
from indicators.rsi import RSI

def test_rsi_calculation():
    # Correct CSV path you provided
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

    # Load CSV
    df = pd.read_csv(csv_path)

    # Make sure CSV has Close column
    assert "Close" in df.columns, "CSV must contain a Close column."

    # Create RSI instance
    rsi = RSI(df, window=14)

    # Run calculation
    result = rsi.calculate()

    # Assertions
    assert "RSI_14" in result.columns, "RSI_14 column missing"
    assert len(result) == len(df), "Output row count mismatch"
    assert result["RSI_14"].dtype.kind in ["f", "i"], "RSI_14 must be numeric"
    assert result["RSI_14"].isna().sum() > 0, "Expected warmup NaN values"
    assert result["RSI_14"].notna().sum() > 0, "RSI returned all NaN values"
