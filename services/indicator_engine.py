from indicators.feature_builder import FeatureBuilder


def apply_indicators(df, use=None):
    """
    Compatibility layer for old tests.

    Parameters
    ----------
    df : pd.DataFrame
        Input OHLCV data.
    use : list[str] or None
        Indicators to use (ignored for now, kept for compatibility).

    Returns
    -------
    tuple:
        (full_df, latest_row)
    """

    if df is None or df.empty:
        raise ValueError("Input DataFrame is empty.")

    # Apply all indicators (new pipeline)
    full_df = FeatureBuilder(df).build()

    # Drop rows with NaNs from indicators
    full_df_clean = full_df.dropna()

    if len(full_df_clean) == 0:
        raise ValueError("No valid rows after applying indicators.")

    # Latest usable row
    latest = full_df_clean.iloc[-1]

    return full_df, latest
