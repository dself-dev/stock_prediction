import pandas as pd
from indicators.sma import SMA


def test_sma_basic():
    df = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 9, 8, 7]
    })

    result = SMA(df).calculate()

    # Check columns exist
    assert "SMA_10" in result.columns
    assert "SMA_20" in result.columns
    assert "SMA_50" in result.columns

    # Output should have same number of rows
    assert len(result) == len(df)
