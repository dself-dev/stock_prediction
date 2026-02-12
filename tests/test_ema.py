import pandas as pd
from pathlib import Path
from indicators.ema import EMA


def test_ema_calculation():
    # I point directly to the same CSV I'm using for all indicator tests
    csv_path = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")

    # I load the CSV into a DataFrame
    df = pd.read_csv(csv_path)

    # I make sure the CSV has the Close column I need for EMA calculations
    assert "Close" in df.columns, "CSV missing required Close column."

    # I create the EMA indicator instance
    ema = EMA(df)

    # I run the EMA calculation
    result = ema.calculate()

    # --- ASSERTIONS ---

    # I expect both EMA_12 and EMA_26 columns to exist after calculation
    assert "EMA_12" in result.columns, "EMA_12 column missing"
    assert "EMA_26" in result.columns, "EMA_26 column missing"

    # Output should have the same number of rows as the input
    assert len(result) == len(df), "EMA output row count mismatch"

    # EMA values must be numeric
    assert result["EMA_12"].dtype.kind in ["f", "i"], "EMA_12 must be numeric"
    assert result["EMA_26"].dtype.kind in ["f", "i"], "EMA_26 must be numeric"

    # I expect at least some actual values (not all NaN)
    assert result["EMA_12"].notna().sum() > 0, "EMA_12 returned all NaN values"
    assert result["EMA_26"].notna().sum() > 0, "EMA_26 returned all NaN values"
