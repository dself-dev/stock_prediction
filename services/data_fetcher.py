import yfinance as yf
import pandas as pd


class DataFetcher:
    """
    Retrieve raw historical market data from yfinance.

    This class is responsible only for data acquisition. It downloads
    OHLCV time-series data for equities or crypto tickers and returns
    the unmodified pandas DataFrame for downstream processing.

    Responsibilities:
    - accept a ticker symbol
    - download historical market data
    - support either a default lookback period or explicit date ranges
    - return the raw dataset as received from yfinance

    Non-responsibilities:
    - data cleaning
    - column standardization
    - index transformation
    - feature engineering
    """

    def __init__(
        self,
        period: str = "5y",
        interval: str = "1d",
        auto_adjust: bool = False,
    ) -> None:
        """
        Initialize download settings used when explicit dates are not provided.

        Args:
            period: Default historical window passed to yfinance.
            interval: Data granularity (for example, 1d, 1h).
            auto_adjust: Whether yfinance should automatically adjust prices.
        """
        self.period = period
        self.interval = interval
        self.auto_adjust = auto_adjust

    def fetch(
        self,
        ticker: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> pd.DataFrame:
        """
        Download historical data for a ticker.

        If both start_date and end_date are provided, the download uses the
        explicit date range. Otherwise, it falls back to the default period
        configured on initialization.

        Args:
            ticker: Market symbol such as AAPL or BTC-USD.
            start_date: Optional inclusive start date in YYYY-MM-DD format.
            end_date: Optional exclusive end date in YYYY-MM-DD format.

        Returns:
            A pandas DataFrame containing raw historical market data.

        Raises:
            ValueError: If the ticker is invalid or no data is returned.
        """
        if not ticker or not isinstance(ticker, str):
            raise ValueError("Ticker must be a non-empty string.")

        ticker = ticker.strip().upper()

        if start_date and end_date:
            df = yf.download(
                ticker,
                start=start_date,
                end=end_date,
                interval=self.interval,
                auto_adjust=self.auto_adjust,
                progress=False,
            )
        else:
            df = yf.download(
                ticker,
                period=self.period,
                interval=self.interval,
                auto_adjust=self.auto_adjust,
                progress=False,
                )

        if df is None or df.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        return df

