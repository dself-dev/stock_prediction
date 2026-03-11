import pandas as pd

class DataCleaner:
    """
    Cleans raw yfinance or CSV DataFrames so they match the clean CSV format
    expected by indicators and the regression pipeline.
    """

    REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]

    def __init__(self, df: pd.DataFrame):
        if df is None or df.empty:
            raise ValueError("DataCleaner received an empty DataFrame.")
        self.df = df.copy()

    # -------------------------------------------------
    # MAIN CLEAN METHOD
    # -------------------------------------------------
    def clean(self) -> pd.DataFrame:
        """
        Normalize and validate yfinance or CSV output.
        Ensures the DF has uppercase OHLCV columns,
        keeps Date if present, and removes unnecessary fields.
        """

        self._flatten_columns()
        self._standardize_column_names()
        self._ensure_required_columns()
        self._drop_extra_columns()
        self._fix_index()

        return self.df.copy()

    # -------------------------------------------------
    # FLATTEN MULTIINDEX FROM YFINANCE
    # -------------------------------------------------
    def _flatten_columns(self):
        """Flatten MultiIndex columns that yfinance sometimes returns."""
        if isinstance(self.df.columns, pd.MultiIndex):
            self.df.columns = [
                col[0] if isinstance(col, tuple) else col
                for col in self.df.columns
            ]

    # -------------------------------------------------
    # STANDARDIZE COLUMN NAMES
    # -------------------------------------------------
    def _standardize_column_names(self):
        """Convert lowercase → Title case and rename common variations."""
        rename_map = {
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "adj close": "Close",
            "volume": "Volume",
            "vol.": "Volume",
        }

        # Normalize to Title case
        self.df.columns = [col.strip().title() for col in self.df.columns]

        # Apply renames
        self.df = self.df.rename(columns=rename_map)

    # -------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # -------------------------------------------------
    def _ensure_required_columns(self):
        """Ensure the DF contains essential OHLCV columns."""
        for col in self.REQUIRED_COLUMNS:
            if col not in self.df.columns:
                raise ValueError(
                    f"Missing required column: '{col}'. "
                    f"Columns present: {list(self.df.columns)}"
                )

    # -------------------------------------------------
    # DROP EXTRA COLUMNS (BUT KEEP DATE)
    # -------------------------------------------------
    def _drop_extra_columns(self):
        """
        Keep ONLY: Date, Open, High, Low, Close, Volume.
        Remove: Dividends, Stock Splits, Adj Close, etc.
        """
        allowed = set(self.REQUIRED_COLUMNS + ["Date"])
        self.df = self.df[[c for c in self.df.columns if c in allowed]]

    # -------------------------------------------------
    # FIX INDEX FOR BOTH CSV AND YFINANCE
    # -------------------------------------------------
    def _fix_index(self):
        """
        Normalize index behavior:
        - If index is DatetimeIndex → keep it (yfinance case)
        - If 'Date' column exists → convert to datetime and set as index
        - If no Date info → leave index as-is (CSV fallback)
        """

        
        if isinstance(self.df.index, pd.DatetimeIndex):
            self.df.index = self.df.index.tz_localize(None)
            return

        # CSV WITH Date column
        if "Date" in self.df.columns:
            self.df["Date"] = pd.to_datetime(self.df["Date"], errors="coerce")
            self.df = self.df.set_index("Date")
            return

        # No Date at all — leave index unchanged
        # (Indicators do not require date)
        return
