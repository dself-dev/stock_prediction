import yfinance as yf
import pandas as pd
import ta


class RSI:
    """Simple RSI class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # RSI (14-period)
            df['RSI_14'] = ta.momentum.rsi(df['Close'], window=14)
        except Exception as e:
            print(f"Error: {e}")


class BollingerBands:
    """Simple Bollinger Bands class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # Bollinger Bands (20-period, 2 std dev)
            df['Bollinger_Upper'] = ta.volatility.bollinger_hband(df['Close'], window=20, window_dev=2)
            df['Bollinger_Middle'] = ta.volatility.bollinger_mavg(df['Close'], window=20)
            df['Bollinger_Lower'] = ta.volatility.bollinger_lband(df['Close'], window=20, window_dev=2)
        except Exception as e:
            print(f"Error: {e}")


class EMA:
    """Simple EMA class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # EMAs (12 and 26 period)
            df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
            df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
        except Exception as e:
            print(f"Error: {e}")


class SMA:
    """Simple SMA class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # SMAs (10, 20, 50 period)
            df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
            df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
            df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
        except Exception as e:
            print(f"Error: {e}")


class MACD:
    """Simple MACD class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # MACD
            df['MACD'] = ta.trend.macd(df['Close'])
            df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])
        except Exception as e:
            print(f"Error: {e}")


class Stochastic:
    """Simple Stochastic class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # Stochastic
            df['Stoch_K'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
            df['Stoch_D'] = ta.momentum.stoch_signal(df['High'], df['Low'], df['Close'])
        except Exception as e:
            print(f"Error: {e}")


class ATR:
    """Simple ATR class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # Average True Range (ATR)
            df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
        except Exception as e:
            print(f"Error: {e}")


class VolumeSMA:
    """Simple Volume SMA class"""
    
    def __init__(self, df):
        """Initialize with dataframe"""
        try:
            # Volume indicators (simple moving average of volume) - FIXED THIS LINE
            df['Volume_SMA'] = ta.trend.sma_indicator(df['Volume'], window=20)
        except Exception as e:
            print(f"Error: {e}")


class SaveData:
    """Simple data saving class"""
    
    def __init__(self, df, ticker_input, interval_input):
        """Initialize and save dataframe"""
        try:
            # Get current date for filename
            from datetime import datetime
            date_str = datetime.now().strftime("%Y%m%d")
            
            # Save to CSV
            path = r"C:\Users\dself\OneDrive\Market_data\CSV"
            filename = f"{path}\\{ticker_input}_{interval_input}_{date_str}_complete.csv"

            df.to_csv(filename, index=False)
            
            print(f"\n✅ Complete dataset saved to {filename}")
            print(f"Shape: {df.shape}")
            print(f"Columns: {list(df.columns)}")
            
            # Show how many NaN values per column
            print("\nNaN counts per column:")
            print(df.isnull().sum())
        except Exception as e:
            print(f"Error: {e}")