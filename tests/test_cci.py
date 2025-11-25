import pandas as pd
from indicators.cci import CCI


def test_cci_basic():
    # Must provide at least 20 rows because window=20
    df = pd.DataFrame({
        "High":  [i + 12 for i in range(20)],
        "Low":   [i + 10 for i in range(20)],
        "Close": [i + 11 for i in range(20)],
    })

    result = CCI(df).calculate()

    assert "CCI_20" in result.columns
    assert len(result) == len(df)
