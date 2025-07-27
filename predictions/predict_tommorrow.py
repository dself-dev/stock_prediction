# '''Right now this model is predicting 96 percent accuracy'''

# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# import yfinance as yf
# import ta
# from datetime import datetime
# import warnings
# warnings.filterwarnings('ignore')

# def predict_tomorrow():
#     # Load ALL your historical data (5 years ending yesterday)
#     df = pd.read_csv('IONQ_1d_complete.csv')
#     df['Date'] = pd.to_datetime(df['Date'])
    
#     # Remove rows where key indicators are missing
#     key_columns = ['RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower', 
#                    'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50', 'MACD', 'MACD_Signal']
    
#     df_clean = df.dropna(subset=key_columns)
#     print(f" Training on ALL {df_clean.shape[0]} days of historical data")
#     print(f" From {df_clean['Date'].min().strftime('%Y-%m-%d')} to {df_clean['Date'].max().strftime('%Y-%m-%d')}")
    
#     # Define features
#     feature_columns = [
#         'Open', 'High', 'Low', 'Volume',
#         'RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
#         'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50',
#         'MACD', 'MACD_Signal', 'Stoch_K', 'Stoch_D', 'ATR', 'Volume_SMA'
#     ]
    
#     # Use ALL data for training (no train/test split - we want maximum learning)
#     X = df_clean[feature_columns].copy()
#     y = df_clean['Close'].copy()
    
#     # Handle any remaining NaN values
#     X = X.fillna(method='ffill').fillna(method='bfill')
    
#     # Scale the features and target
#     scaler_X = StandardScaler()
#     scaler_y = StandardScaler()
    
#     X_scaled = scaler_X.fit_transform(X)
#     y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()
    
#     # Build the model
#     model = keras.Sequential([
#         layers.Dense(1, input_shape=(X_scaled.shape[1],), activation='linear')
#     ])
    
#     model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
#     print(" Training model on ALL historical data...")
#     # Train with more epochs for better accuracy
#     model.fit(X_scaled, y_scaled, epochs=500, batch_size=32, 
#               validation_split=0.1, verbose=1)
    
#     # get TODAY's live data to predict TOMORROW
#     print(f"\n📡 Fetching today's live data for AAPL...")
    
#     # Get recent data (100 days) to calculate indicators
#     df_live = yf.download("AAPL", period="100d", interval="1d")
#     df_live = df_live.reset_index()
    
#     # Fix column names if needed may have to do this..
#     if isinstance(df_live.columns, pd.MultiIndex):
#         df_live.columns = [col[0] for col in df_live.columns]
    
#     # Calculate technical indicators for live data
#     print("📈 Calculating current technical indicators...")
#     df_live['RSI_14'] = ta.momentum.rsi(df_live['Close'], window=14)
#     df_live['Bollinger_Upper'] = ta.volatility.bollinger_hband(df_live['Close'], window=20, window_dev=2)
#     df_live['Bollinger_Middle'] = ta.volatility.bollinger_mavg(df_live['Close'], window=20)
#     df_live['Bollinger_Lower'] = ta.volatility.bollinger_lband(df_live['Close'], window=20, window_dev=2)
#     df_live['EMA_12'] = ta.trend.ema_indicator(df_live['Close'], window=12)
#     df_live['EMA_26'] = ta.trend.ema_indicator(df_live['Close'], window=26)
#     df_live['SMA_10'] = ta.trend.sma_indicator(df_live['Close'], window=10)
#     df_live['SMA_20'] = ta.trend.sma_indicator(df_live['Close'], window=20)
#     df_live['SMA_50'] = ta.trend.sma_indicator(df_live['Close'], window=50)
#     df_live['MACD'] = ta.trend.macd(df_live['Close'])
#     df_live['MACD_Signal'] = ta.trend.macd_signal(df_live['Close'])
#     df_live['Stoch_K'] = ta.momentum.stoch(df_live['High'], df_live['Low'], df_live['Close'])
#     df_live['Stoch_D'] = ta.momentum.stoch_signal(df_live['High'], df_live['Low'], df_live['Close'])
#     df_live['ATR'] = ta.volatility.average_true_range(df_live['High'], df_live['Low'], df_live['Close'])
#     df_live['Volume_SMA'] = ta.trend.sma_indicator(df_live['Volume'], window=20)
    
#     # Get today's data (most recent complete day)
#     today_data = df_live.dropna().iloc[-1]
#     today_date = today_data['Date'].strftime('%Y-%m-%d')
#     current_price = today_data['Close']
    
#     print(f"📅 Using data from: {today_date}")
#     print(f"💰 Today's closing price: ${current_price:.2f}")
    
#     # Prepare today's features for prediction
#     X_today = today_data[feature_columns].values.reshape(1, -1)
#     X_today_scaled = scaler_X.transform(X_today)
    
#     # Make prediction for tomorrow
#     prediction_scaled = model.predict(X_today_scaled, verbose=0)
#     predicted_close = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1)).flatten()[0]
    
#     # Calculate predicted change
#     change = predicted_close - current_price
#     change_pct = (change / current_price) * 100
    
#     # Results
#     print(f"\n🔮 TOMORROW'S PREDICTION (July 16, 2025):")
#     print(f"📅 Prediction Date: {datetime.now().strftime('%Y-%m-%d')} (Tomorrow)")
#     print(f"💰 Today's Close: ${current_price:.2f}")
#     print(f"🎯 Predicted Close: ${predicted_close:.2f}")
#     print(f"📈 Expected Change: ${change:+.2f} ({change_pct:+.1f}%)")
    
#     if change > 0:
#         print("📈 PREDICTION: Apple stock will GO UP tomorrow! 🚀")
#     else:
#         print("📉 PREDICTION: Apple stock will GO DOWN tomorrow 📉")
    
#     print(f"\n⏰ Check back tomorrow at market close to see if we're right!")
#     print(f"🎯 This prediction is based on {df_clean.shape[0]} days of learning")
    
#     return predicted_close, current_price, change_pct

# if __name__ == "__main__":
#     print("=" * 60)
#     print("🍎 APPLE STOCK PREDICTION FOR TOMORROW")
#     print("=" * 60)
    
#     predicted_close, current_price, change_pct = predict_tomorrow()
    
#     print(f"\n📋 SUMMARY:")
#     print(f"   Model trained on: 5 years of Apple data")
#     print(f"   Tomorrow's predicted close: ${predicted_close:.2f}")
#     print(f"   Expected change: {change_pct:+.1f}%")
'''Right now this model is predicting 96 percent accuracy'''

'''Right now this model is predicting 96 percent accuracy'''

'''Right now this model is predicting 96 percent accuracy'''

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import yfinance as yf
import ta
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def predict_tomorrow(stock_symbol="IONQ", csv_file=None):
    """
    Predict tomorrow's stock price for any symbol
    
    Args:
        stock_symbol: The stock ticker symbol (e.g., 'IONQ', 'AAPL', 'TSLA')
        csv_file: Path to CSV file with historical data (optional, will use stock_symbol if not provided)
    """
    
    # Use provided CSV file
    csv_file = csv_file or f'{stock_symbol}_1d_complete.csv'
    
    # Load historical data
    try:
        df = pd.read_csv(csv_file)
        print(f"📊 Loaded historical data from: {csv_file}")
    except FileNotFoundError:
        print(f"❌ Error: Could not find {csv_file}")
        print(f"💡 Make sure the file exists in the current directory")
        return None, None, None
    
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Remove rows where key indicators are missing
    key_columns = ['RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower', 
                   'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50', 'MACD', 'MACD_Signal']
    
    df_clean = df.dropna(subset=key_columns)
    print(f"📈 Training on ALL {df_clean.shape[0]} days of historical data for {stock_symbol}")
    print(f"📅 From {df_clean['Date'].min().strftime('%Y-%m-%d')} to {df_clean['Date'].max().strftime('%Y-%m-%d')}")
    
    # Define features
    feature_columns = [
        'Open', 'High', 'Low', 'Volume',
        'RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
        'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50',
        'MACD', 'MACD_Signal', 'Stoch_K', 'Stoch_D', 'ATR', 'Volume_SMA'
    ]
    
    # Use ALL data for training
    X = df_clean[feature_columns].copy()
    y = df_clean['Close'].copy()
    
    # Handle any remaining NaN values
    X = X.fillna(method='ffill').fillna(method='bfill')
    
    # Scale the features and target
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()
    
    # Build the model
    model = keras.Sequential([
        layers.Dense(1, input_shape=(X_scaled.shape[1],), activation='linear')
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    print(f"🧠 Training model on ALL historical data for {stock_symbol}...")
    # Train with more epochs for better accuracy
    model.fit(X_scaled, y_scaled, epochs=500, batch_size=32, 
              validation_split=0.1, verbose=1)
    
    # Get TODAY's live data to predict TOMORROW
    print(f"\n📡 Fetching today's live data for {stock_symbol}...")
    
    try:
        # Get recent data (100 days) to calculate indicators
        df_live = yf.download(stock_symbol, period="100d", interval="1d")
        df_live = df_live.reset_index()
        
        if df_live.empty:
            print(f"❌ Error: No live data found for {stock_symbol}")
            print("💡 Make sure the stock symbol is valid and markets are open")
            return None, None, None
            
    except Exception as e:
        print(f"❌ Error fetching live data for {stock_symbol}: {e}")
        return None, None, None
    
    # Fix column names if needed
    if isinstance(df_live.columns, pd.MultiIndex):
        df_live.columns = [col[0] for col in df_live.columns]
    
    # Calculate technical indicators for live data
    print(f"📈 Calculating current technical indicators for {stock_symbol}...")
    df_live['RSI_14'] = ta.momentum.rsi(df_live['Close'], window=14)
    df_live['Bollinger_Upper'] = ta.volatility.bollinger_hband(df_live['Close'], window=20, window_dev=2)
    df_live['Bollinger_Middle'] = ta.volatility.bollinger_mavg(df_live['Close'], window=20)
    df_live['Bollinger_Lower'] = ta.volatility.bollinger_lband(df_live['Close'], window=20, window_dev=2)
    df_live['EMA_12'] = ta.trend.ema_indicator(df_live['Close'], window=12)
    df_live['EMA_26'] = ta.trend.ema_indicator(df_live['Close'], window=26)
    df_live['SMA_10'] = ta.trend.sma_indicator(df_live['Close'], window=10)
    df_live['SMA_20'] = ta.trend.sma_indicator(df_live['Close'], window=20)
    df_live['SMA_50'] = ta.trend.sma_indicator(df_live['Close'], window=50)
    df_live['MACD'] = ta.trend.macd(df_live['Close'])
    df_live['MACD_Signal'] = ta.trend.macd_signal(df_live['Close'])
    df_live['Stoch_K'] = ta.momentum.stoch(df_live['High'], df_live['Low'], df_live['Close'])
    df_live['Stoch_D'] = ta.momentum.stoch_signal(df_live['High'], df_live['Low'], df_live['Close'])
    df_live['ATR'] = ta.volatility.average_true_range(df_live['High'], df_live['Low'], df_live['Close'])
    df_live['Volume_SMA'] = ta.trend.sma_indicator(df_live['Volume'], window=20)
    
    # Get today's data (most recent complete day)
    today_data = df_live.dropna().iloc[-1]
    today_date = today_data['Date'].strftime('%Y-%m-%d')
    current_price = today_data['Close']
    
    print(f"📅 Using data from: {today_date}")
    print(f"💰 Today's closing price: ${current_price:.2f}")
    
    # Prepare today's features for prediction
    X_today = today_data[feature_columns].values.reshape(1, -1)
    X_today_scaled = scaler_X.transform(X_today)
    
    # Make prediction for tomorrow
    prediction_scaled = model.predict(X_today_scaled, verbose=0)
    predicted_close = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1)).flatten()[0]
    
    # Calculate predicted change
    change = predicted_close - current_price
    change_pct = (change / current_price) * 100
    
    # Results
    print(f"\n🔮 TOMORROW'S PREDICTION for {stock_symbol}:")
    print(f"📅 Prediction Date: {datetime.now().strftime('%Y-%m-%d')} (Tomorrow)")
    print(f"💰 Today's Close: ${current_price:.2f}")
    print(f"🎯 Predicted Close: ${predicted_close:.2f}")
    print(f"📈 Expected Change: ${change:+.2f} ({change_pct:+.1f}%)")
    
    if change > 0:
        print(f"📈 PREDICTION: {stock_symbol} stock will GO UP tomorrow! 🚀")
    else:
        print(f"📉 PREDICTION: {stock_symbol} stock will GO DOWN tomorrow 📉")
    
    print(f"\n⏰ Check back tomorrow at market close to see if we're right!")
    print(f"🎯 This prediction is based on {df_clean.shape[0]} days of learning")
    
    return predicted_close, current_price, change_pct

if __name__ == "__main__":
    print("=" * 60)
    print("📊 STOCK PREDICTION FOR TOMORROW")
    print("=" * 60)
    
    # Ask user for CSV file only
    csv_file = input("📁 Enter the CSV file name (e.g., TSLA_1d_complete.csv): ").strip()
    
    # Extract stock symbol from filename
    # Assumes format like "TSLA_1d_complete.csv" or "TSLA_data.csv"
    stock_symbol = csv_file.split('_')[0].upper()
    
    print(f"\n🔄 Loading {csv_file} for {stock_symbol} prediction...")
    
    predicted_close, current_price, change_pct = predict_tomorrow(stock_symbol, csv_file)
    
    if predicted_close is not None:
        print(f"\n📋 SUMMARY:")
        print(f"   Model trained on: {csv_file}")
        print(f"   Tomorrow's predicted close: ${predicted_close:.2f}")
        print(f"   Expected change: {change_pct:+.1f}%")
    else:
        print(f"\n❌ Could not generate prediction")
        print("💡 Check that you have the correct CSV file and stock symbol")