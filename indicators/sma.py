import yfinance as yf
import pandas as pd
import ta

# Ask user for inputs
ticker_input = input("Enter ticker symbol (e.g. AAPL, IONQ): ").upper()
interval_input = input("Enter interval (e.g. 1d, 1h, 30m, 15m): ").lower()

# Optional: Ask for how much data
if interval_input == "1d":
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    df = yf.download(ticker_input, start=start_date, end=end_date, interval=interval_input)
else:
    period = input("Enter how far back (e.g. 730d, 90d, 2y): ")
    df = yf.download(ticker_input, period=period, interval=interval_input)

# Reset index to get Date as a column
df = df.reset_index()

# Fix column names (yfinance sometimes returns multi-level columns)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [col[0] for col in df.columns]

# Make sure we have the right column names
print("Columns:", df.columns.tolist())

# Calculate technical indicators
print("Calculating technical indicators...")

# RSI (14-period)
df['RSI_14'] = ta.momentum.rsi(df['Close'], window=14)

# Bollinger Bands (20-period, 2 std dev)
df['Bollinger_Upper'] = ta.volatility.bollinger_hband(df['Close'], window=20, window_dev=2)
df['Bollinger_Middle'] = ta.volatility.bollinger_mavg(df['Close'], window=20)
df['Bollinger_Lower'] = ta.volatility.bollinger_lband(df['Close'], window=20, window_dev=2)

# EMAs (12 and 26 period)
df['EMA_12'] = ta.trend.ema_indicator(df['Close'], window=12)
df['EMA_26'] = ta.trend.ema_indicator(df['Close'], window=26)

# SMAs (10, 20, 50 period)
df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)

# MACD
df['MACD'] = ta.trend.macd(df['Close'])
df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])

# Stochastic
df['Stoch_K'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
df['Stoch_D'] = ta.momentum.stoch_signal(df['High'], df['Low'], df['Close'])

# Average True Range (ATR)
df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])

# Volume indicators (simple moving average of volume)
df['Volume_SMA'] = ta.trend.sma_indicator(df['Volume'], window=20)

# Show preview
print("\nPreview of data with all indicators:")
print(df.head(10))

# Save to CSV
filename = f"{ticker_input}_{interval_input}_complete.csv"
df.to_csv(filename, index=False)

print(f"\n✅ Complete dataset saved to {filename}")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Show how many NaN values per column
print("\nNaN counts per column:")
print(df.isnull().sum())

print(f"\n🚀 Ready for Jupyter! Load with: df = pd.read_csv('{filename}')")