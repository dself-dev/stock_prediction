import pandas as pd
from pathlib import Path
from indicators.macd import MACD


def test_macd_calculation():
    # I point to the same CSV I use for the rest of my indicator tests
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

    # I load the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # Make sure the CSV has the Close column needed for MACD
    assert "Close" in df.columns, "CSV missing required Close column."

    # I create the MACD indicator instance
    macd = MACD(df)

    # I run the MACD calculation
    result = macd.calculate()

    # --- ASSERTIONS ---

    # Make sure all three MACD columns exist
    assert "MACD" in result.columns, "MACD column missing"
    assert "MACD_Signal" in result.columns, "MACD_Signal column missing"
    assert "MACD_Histogram" in result.columns, "MACD_Histogram column missing"

    # The output row count should match the input row count
    assert len(result) == len(df), "MACD output row count mismatch"

    # MACD values must be numeric
    assert result["MACD"].dtype.kind in ["f", "i"], "MACD must be numeric"
    assert result["MACD_Signal"].dtype.kind in ["f", "i"], "MACD_Signal must be numeric"
    assert result["MACD_Histogram"].dtype.kind in ["f", "i"], "MACD_Histogram must be numeric"

    # I expect at least some real values for each column
    assert result["MACD"].notna().sum() > 0, "MACD returned all NaN values"
    assert result["MACD_Signal"].notna().sum() > 0, "MACD_Signal returned all NaN values"
    assert result["MACD_Histogram"].notna().sum() > 0, "MACD_Histogram returned all NaN values"
