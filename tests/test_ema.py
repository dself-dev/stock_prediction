import pandas as pd
from indicators.ema import EMA


def test_ema_basic():
    df = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 9, 8, 7]
    })

    result = EMA(df).calculate()

    # Check EMA columns exist
    assert "EMA_12" in result.columns
    assert "EMA_26" in result.columns

    # Should return same number of rows
    assert len(result) == len(df)
