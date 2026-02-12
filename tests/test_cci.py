import pandas as pd
from pathlib import Path
from indicators.cci import CCI


def test_cci_calculation():
    # I point directly to the same CSV I’ve been using for all my indicator tests
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

    # I load the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # I make sure the CSV has the required columns for CCI
    required = {"High", "Low", "Close"}
    for col in required:
        assert col in df.columns, f"CSV missing required column: {col}"

    # I create the CCI indicator instance
    cci = CCI(df)

    # I run the CCI calculation
    result = cci.calculate()

    # --- ASSERTIONS ---

    # I expect the CCI_20 column to be created
    assert "CCI_20" in result.columns, "CCI_20 column missing"

    # The output should have the same number of rows as the input
    assert len(result) == len(df), "CCI output row count mismatch"

    # CCI values should always be numeric
    assert result["CCI_20"].dtype.kind in ["f", "i"], "CCI_20 must be numeric"

    # I expect at least some real values (not all NaN)
    assert result["CCI_20"].notna().sum() > 0, "CCI returned all NaN values"
