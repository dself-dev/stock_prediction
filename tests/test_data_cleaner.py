import pandas as pd
from data_pipeline.data_cleaner import DataCleaner

def test_data_cleaner_with_csv():
    df = pd.read_csv("test_csv/AAPL_2022-01-01_to_2025-10-27.csv")

    cleaner = DataCleaner(df)
    clean_df = cleaner.clean()

    # Confirm required columns exist
    assert "Open" in clean_df.columns
    assert "High" in clean_df.columns
    assert "Low" in clean_df.columns
    assert "Close" in clean_df.columns
    assert "Volume" in clean_df.columns

    # Make sure no extra columns exist
    assert set(clean_df.columns) == {"Open", "High", "Low", "Close", "Volume"}
