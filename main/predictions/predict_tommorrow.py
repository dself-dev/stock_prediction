

"""
predict_tomorrow.py
Live forecast script: predicts tomorrow's stock price AND sentiment.
"""

import os
import sys
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras import layers
import yfinance as yf
import ta
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# --- Fix import path so services works ---
# Go up 2 levels from main/predictions into project root (Market_data)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.sentiment import scrape_yahoo_news, score_with_vader


def predict_tomorrow(stock_symbol: str):
    """
    Predict tomorrow's stock price and get sentiment for the ticker.
    """

    # --- Load historical data (CSV or Yahoo Finance) ---
    csv_file = f"{stock_symbol}_1d_complete.csv"
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        print(f" Loaded historical data from: {csv_file}")
    else:
        print(f" No CSV found for {stock_symbol}, downloading with yfinance...")
        df = yf.download(stock_symbol, period="2y", interval="1d")
        df = df.reset_index()
        df.to_csv(csv_file, index=False)

    # --- Fix column issues ---
    df['Date'] = pd.to_datetime(df['Date'])

    # Flatten MultiIndex columns if Yahoo gives them (e.g., AAPL sometimes)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

    # Ensure numeric types for price/volume data
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- Technical Indicators ---
    df['RSI_14'] = ta.momentum.rsi(df['Close'], window=14)
    df['Bollinger_Upper'] = ta.volatility.bollinger_hband(df['Close'])
    df['Bollinger_Middle'] = ta.volatility.bollinger_mavg(df['Close'])
    df['Bollinger_Lower'] = ta.volatility.bollinger_lband(df['Close'])
    df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
    df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)
    df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
    df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)
    df['MACD'] = ta.trend.macd(df['Close'])
    df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])
    df['Stoch_K'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
    df['Stoch_D'] = ta.momentum.stoch_signal(df['High'], df['Low'], df['Close'])
    df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
    df['Volume_SMA'] = ta.trend.sma_indicator(df['Volume'], window=20)

    key_columns = [
        'RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
        'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50', 'MACD', 'MACD_Signal'
    ]

    df_clean = df.dropna(subset=key_columns)

    feature_columns = [
        'Open', 'High', 'Low', 'Volume',
        'RSI_14', 'Bollinger_Upper', 'Bollinger_Middle', 'Bollinger_Lower',
        'EMA_12', 'EMA_26', 'SMA_10', 'SMA_20', 'SMA_50',
        'MACD', 'MACD_Signal', 'Stoch_K', 'Stoch_D', 'ATR', 'Volume_SMA'
    ]

    # --- Training Data ---
    X = df_clean[feature_columns].fillna(method='ffill').fillna(method='bfill')
    y = df_clean['Close']

    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.values.reshape(-1, 1)).flatten()

    # --- Model ---
    model = keras.Sequential([
        layers.Dense(1, input_shape=(X_scaled.shape[1],), activation='linear')
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    print(f" Training model on {df_clean.shape[0]} days of data for {stock_symbol}...")
    model.fit(X_scaled, y_scaled, epochs=100, batch_size=32, validation_split=0.1, verbose=0)

    # --- Predict Tomorrow ---
    today_data = df_clean.iloc[-1]
    current_price = today_data['Close']
    today_date = today_data['Date'].strftime('%Y-%m-%d')

    X_today = today_data[feature_columns].values.reshape(1, -1)
    X_today_scaled = scaler_X.transform(X_today)

    prediction_scaled = model.predict(X_today_scaled, verbose=0)
    predicted_close = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1)).flatten()[0]

    change = predicted_close - current_price
    change_pct = (change / current_price) * 100

    # --- Sentiment ---
    print(f"\n Scraping sentiment for {stock_symbol}...")
    news_result = scrape_yahoo_news(stock_symbol, limit=3, headless=True)
    sentiment = score_with_vader(news_result["saved_to"])

    # --- Report ---
    print("\n" + "=" * 60)
    print(f" TOMORROW'S FORECAST for {stock_symbol}")
    print("=" * 60)
    print(f" Date: {today_date}")
    print(f" Today's Close: ${current_price:.2f}")
    print(f" Predicted Close: ${predicted_close:.2f}")
    print(f" Expected Change: {change:+.2f} ({change_pct:+.1f}%)")

    if change > 0:
        print(" ML Prediction: GO UP")
    else:
        print(" ML Prediction: GO DOWN")

    print(f"\n Sentiment: {sentiment['label'].upper()} "
          f"(avg score {sentiment['avg_sentiment']:.3f})")

    # --- Final Combined Summary since sediment can change price drastically I wanted to add warning t his will be imporved in future for better predicton though ---
    if (change > 0 and sentiment['label'] == "positive") or (change < 0 and sentiment['label'] == "negative"):
        print(" ML and Sentiment AGREE -> Stronger Signal")
    else:
        print(" ML and Sentiment DISAGREE -> Mixed Signal, be cautious")

    print("=" * 60)

    return predicted_close, current_price, change_pct, sentiment


if __name__ == "__main__":
    print("=" * 60)
    print("STOCK PREDICTION WITH SENTIMENT")
    print("=" * 60)

    ticker = input("  Enter stock ticker (e.g., AAPL, TSLA, IONQ): ").strip().upper()
    predict_tomorrow(ticker)
