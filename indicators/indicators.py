# import yfinance as yf
# import pandas as pd
# import ta


# class RSI:
#     """Simple RSI class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # RSI (14-period)
#             df['RSI_14'] = ta.momentum.rsi(df['Close'], window=14)
#         except Exception as e:
#             print(f"Error: {e}")


# class BollingerBands:
#     """Simple Bollinger Bands class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # Bollinger Bands (20-period, 2 std dev)
#             df['Bollinger_Upper'] = ta.volatility.bollinger_hband(df['Close'], window=20, window_dev=2)
#             df['Bollinger_Middle'] = ta.volatility.bollinger_mavg(df['Close'], window=20)
#             df['Bollinger_Lower'] = ta.volatility.bollinger_lband(df['Close'], window=20, window_dev=2)
#         except Exception as e:
#             print(f"Error: {e}")


# class EMA:
#     """Simple EMA class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # EMAs (12 and 26 period)
#             df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
#             df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
#         except Exception as e:
#             print(f"Error: {e}")


# class SMA:
#     """Simple SMA class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # SMAs (10, 20, 50 period)
#             df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
#             df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
#             df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
#         except Exception as e:
#             print(f"Error: {e}")


# class MACD:
#     """Simple MACD class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # MACD
#             df['MACD'] = ta.trend.macd(df['Close'])
#             df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])
#         except Exception as e:
#             print(f"Error: {e}")


# class Stochastic:
#     """Simple Stochastic class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # Stochastic
#             df['Stoch_K'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
#             df['Stoch_D'] = ta.momentum.stoch_signal(df['High'], df['Low'], df['Close'])
#         except Exception as e:
#             print(f"Error: {e}")


# class ATR:
#     """Simple ATR class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # Average True Range (ATR)
#             df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
#         except Exception as e:
#             print(f"Error: {e}")


# class VolumeSMA:
#     """Simple Volume SMA class"""
    
#     def __init__(self, df):
#         """Initialize with dataframe"""
#         try:
#             # Volume indicators (simple moving average of volume) - FIXED THIS LINE
#             df['Volume_SMA'] = ta.trend.sma_indicator(df['Volume'], window=20)
#         except Exception as e:
#             print(f"Error: {e}")


# class SaveData:
#     """Simple data saving class"""
    
#     def __init__(self, df, ticker_input, interval_input):
#         """Initialize and save dataframe"""
#         try:
#             # Get current date for filename
#             from datetime import datetime
#             date_str = datetime.now().strftime("%Y%m%d")
            
#             # Save to CSV
#             path = r"C:\Users\dself\OneDrive\Market_data\CSV"
#             filename = f"{path}\\{ticker_input}_{interval_input}_{date_str}_complete.csv"

#             df.to_csv(filename, index=False)
            
#             print(f"\n✅ Complete dataset saved to {filename}")
#             print(f"Shape: {df.shape}")
#             print(f"Columns: {list(df.columns)}")
            
#             # Show how many NaN values per column
#             print("\nNaN counts per column:")
#             print(df.isnull().sum())
#         except Exception as e:
#             print(f"Error: {e}")

import logging
import pandas as pd
import yfinance as yf
import ta
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class RSI:
    """Compute the 14-period Relative Strength Index (RSI)."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds an RSI column to the provided price dataframe.

        Args:
            df (pd.DataFrame): DataFrame containing at least 'Close' column.
        """
        try:
            if "Close" not in df.columns:
                raise ValueError("DataFrame missing required column: 'Close'")

            df["RSI_14"] = ta.momentum.rsi(df["Close"], window=14)

        except Exception as e:
            logging.error(f"RSI calculation error: {e}")


class BollingerBands:
    """Compute Bollinger Bands using a 20-period window and 2 standard deviations."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds Bollinger Upper, Middle, and Lower bands to the dataframe.

        Args:
            df (pd.DataFrame): DataFrame with at least 'Close'.
        """
        try:
            if "Close" not in df.columns:
                raise ValueError("DataFrame missing required column: 'Close'")

            df["Bollinger_Upper"] = ta.volatility.bollinger_hband(df["Close"], window=20, window_dev=2)
            df["Bollinger_Middle"] = ta.volatility.bollinger_mavg(df["Close"], window=20)
            df["Bollinger_Lower"] = ta.volatility.bollinger_lband(df["Close"], window=20, window_dev=2)

        except Exception as e:
            logging.error(f"Bollinger Bands calculation error: {e}")


class EMA:
    """Compute Exponential Moving Averages (EMA 12 and EMA 26)."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds EMA_12 and EMA_26 to the dataframe.

        Args:
            df (pd.DataFrame): DataFrame containing 'Close'.
        """
        try:
            if "Close" not in df.columns:
                raise ValueError("Missing 'Close' column")

            df["EMA_12"] = ta.trend.ema_indicator(df["Close"], window=12)
            df["EMA_26"] = ta.trend.ema_indicator(df["Close"], window=26)

        except Exception as e:
            logging.error(f"EMA calculation error: {e}")


class SMA:
    """Compute Simple Moving Averages (10, 20, and 50 periods)."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds SMA_10, SMA_20, and SMA_50 to the dataframe.

        Args:
            df (pd.DataFrame): DataFrame containing 'Close'.
        """
        try:
            if "Close" not in df.columns:
                raise ValueError("Missing 'Close' column")

            df["SMA_10"] = ta.trend.sma_indicator(df["Close"], window=10)
            df["SMA_20"] = ta.trend.sma_indicator(df["Close"], window=20)
            df["SMA_50"] = ta.trend.sma_indicator(df["Close"], window=50)

        except Exception as e:
            logging.error(f"SMA calculation error: {e}")


class MACD:
    """Compute MACD and MACD Signal Line."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds MACD and MACD_Signal to the dataframe.

        Args:
            df (pd.DataFrame): DataFrame containing 'Close'.
        """
        try:
            if "Close" not in df.columns:
                raise ValueError("Missing 'Close' column")

            df["MACD"] = ta.trend.macd(df["Close"])
            df["MACD_Signal"] = ta.trend.macd_signal(df["Close"])

        except Exception as e:
            logging.error(f"MACD calculation error: {e}")


class Stochastic:
    """Compute Stochastic Oscillator (%K and %D)."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds Stoch_K and Stoch_D to the dataframe.

        Args:
            df (pd.DataFrame): Must contain 'High', 'Low', 'Close'.
        """
        try:
            for col in ("High", "Low", "Close"):
                if col not in df.columns:
                    raise ValueError(f"Missing '{col}' column")

            df["Stoch_K"] = ta.momentum.stoch(df["High"], df["Low"], df["Close"])
            df["Stoch_D"] = ta.momentum.stoch_signal(df["High"], df["Low"], df["Close"])

        except Exception as e:
            logging.error(f"Stochastic calculation error: {e}")


class ATR:
    """Compute Average True Range (ATR)."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds ATR column to the dataframe.

        Args:
            df (pd.DataFrame): Must contain 'High', 'Low', 'Close'.
        """
        try:
            for col in ("High", "Low", "Close"):
                if col not in df.columns:
                    raise ValueError(f"Missing '{col}' column")

            df["ATR"] = ta.volatility.average_true_range(df["High"], df["Low"], df["Close"])

        except Exception as e:
            logging.error(f"ATR calculation error: {e}")


class VolumeSMA:
    """Compute Simple Moving Average of Volume (20-day)."""

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Adds Volume_SMA to the dataframe.

        Args:
            df (pd.DataFrame): Must contain 'Volume'.
        """
        try:
            if "Volume" not in df.columns:
                raise ValueError("Missing 'Volume' column")

            df["Volume_SMA"] = ta.trend.sma_indicator(df["Volume"], window=20)

        except Exception as e:
            logging.error(f"Volume SMA error: {e}")


class SaveData:
    """Save the enriched dataset to CSV."""

    def __init__(self, df: pd.DataFrame, ticker_input: str, interval_input: str, path: Optional[str] = None) -> None:
        """
        Saves the DataFrame to a timestamped CSV file.

        Args:
            df (pd.DataFrame): Dataframe to save.
            ticker_input (str): Stock ticker symbol.
            interval_input (str): Interval string (e.g., '1d').
            path (str, optional): Directory to save CSV. Defaults to your OneDrive path.
        """
        try:
            from datetime import datetime

            default_path = r"C:\Users\dself\OneDrive\Market_data\CSV"
            save_path = path or default_path

            date_str = datetime.now().strftime("%Y%m%d")
            filename = f"{save_path}\\{ticker_input}_{interval_input}_{date_str}_complete.csv"

            df.to_csv(filename, index=False)

            logging.info(f"Dataset saved to {filename}")
            logging.info(f"Shape: {df.shape}")
            logging.info(f"Columns: {list(df.columns)}")
            logging.info("NaN counts per column:")
            logging.info(df.isnull().sum())

        except Exception as e:
            logging.error(f"File save error: {e}")
