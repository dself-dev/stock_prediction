import pandas as pd
from indicators.mfi import MFI


def test_mfi_basic():
    df = pd.DataFrame({
        "High":    [12, 13, 14, 15, 16, 17, 16, 15, 14, 13],
        "Low":     [10, 10, 11, 12, 12, 13, 12, 11, 10,  9],
        "Close":   [11, 12, 13, 14, 15, 16, 15, 14, 13, 12],
        "Volume":  [1000, 1200, 1500, 2000, 1800, 1700, 1600, 1500, 1400, 1300]
    })

    result = MFI(df).calculate()

    assert "MFI_14" in result.columns
    assert len(result) == len(df)
