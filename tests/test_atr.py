import pandas as pd
from indicators.atr import ATR


def test_atr_basic():
    df = pd.DataFrame({
        "High":  [12, 13, 14, 15, 16, 17, 16, 15, 14, 13, 12, 13, 14, 15],
        "Low":   [10, 10, 11, 12, 12, 13, 12, 11, 10,  9,  8,  9, 10, 11],
        "Close": [11, 12, 13, 14, 15, 16, 15, 14, 13, 12, 11, 12, 13, 14]
    })

    result = ATR(df).calculate()

    assert "ATR_14" in result.columns
    assert len(result) == len(df)
