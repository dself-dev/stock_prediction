import pandas as pd
from indicators.rsi import RSI

def test_rsi_basic():
    df = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 9, 8, 7]
    })

    result = RSI(df).calculate()

    assert "RSI_14" in result.columns
    assert len(result) == len(df)
