import pandas as pd
from indicators.bollinger import Bollinger


def test_bollinger_basic():
    df = pd.DataFrame({
        "Close": [10, 11, 12, 13, 12, 11, 10, 9, 8, 7]
    })

    result = Bollinger(df).calculate()

    # Columns should exist
    assert "Bollinger_Upper" in result.columns
    assert "Bollinger_Middle" in result.columns
    assert "Bollinger_Lower" in result.columns

    # Shape should match
    assert len(result) == len(df)
