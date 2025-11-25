import pandas as pd
from indicators.macd import MACD


def test_macd_basic():
    df = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 9, 8, 7]
    })

    result = MACD(df).calculate()

    # Columns should exist
    assert "MACD" in result.columns
    assert "MACD_Signal" in result.columns
    assert "MACD_Histogram" in result.columns

    # Shape should match
    assert len(result) == len(df)
