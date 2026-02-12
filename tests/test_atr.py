import pandas as pd
from pathlib import Path
from indicators.atr import ATR


def test_atr_calculation():
    # I point directly to the CSV file I generated for testing
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

   

    # I load the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # I make sure the CSV has the required OHLC columns before running ATR
    required = {"High", "Low", "Close"}
    for col in required:
        assert col in df.columns, f"CSV missing required column: {col}"

    # I create the ATR instance with the loaded DataFrame
    atr = ATR(df)

    # I run the ATR calculation
    result = atr.calculate()

    # --- ASSERTIONS ---

    # I expect the ATR_14 column to exist after calculation
    assert "ATR_14" in result.columns, "ATR_14 column missing"

    # The ATR DataFrame must have the same number of rows as the original
    assert len(result) == len(df), "ATR output row count mismatch"

    # ATR values should always be numeric (no strings allowed)
    assert result["ATR_14"].dtype.kind in ["f", "i"], "ATR_14 must be numeric"

    # ATR does not produce NaN warmup values, but I still expect at least some positive values
    assert (result["ATR_14"] > 0).any(), "ATR should produce non-zero values"
