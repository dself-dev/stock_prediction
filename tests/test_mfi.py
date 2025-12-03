import pandas as pd
from pathlib import Path
from indicators.mfi import MFI


def test_mfi_calculation():
    # I point to the new CSV I generated that includes Volume
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")


    # I load the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # I make sure the CSV has the required columns for MFI
    required = {"High", "Low", "Close", "Volume"}
    for col in required:
        assert col in df.columns, f"CSV missing required column: {col}"

    # I create the MFI indicator instance
    mfi = MFI(df)

    # I run the MFI calculation
    result = mfi.calculate()

    # --- ASSERTIONS ---

    # I expect the MFI_14 column to exist after calculation
    assert "MFI_14" in result.columns, "MFI_14 column missing"

    # The output row count must match the input
    assert len(result) == len(df), "MFI output row count mismatch"

    # MFI values must be numeric
    assert result["MFI_14"].dtype.kind in ["f", "i"], "MFI_14 must be numeric"

    # I expect at least some actual values (not all NaN)
    assert result["MFI_14"].notna().sum() > 0, "MFI_14 returned all NaN values"
