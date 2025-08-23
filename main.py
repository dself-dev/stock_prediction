import yfinance as yf
import pandas as pd
from indicators.indicators import RSI, BollingerBands, EMA, SMA, MACD, Stochastic, ATR, VolumeSMA, SaveData

# Ask user for inputs
ticker_input = input("Enter ticker symbol (e.g. AAPL, IONQ): ").upper()
interval_input = input("Enter interval (e.g. 1d, 1h, 30m, 15m): ").lower()

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

# Apply all indicators
RSI(df)
BollingerBands(df)
EMA(df)
SMA(df)
MACD(df)
Stochastic(df)
ATR(df)
VolumeSMA(df)

# Save data
SaveData(df, ticker_input, interval_input)