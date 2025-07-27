import yfinance as yf
import pandas as pd


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

# Show preview and save
print(df.head())
filename = f"{ticker_input}_{interval_input}.csv"
df.to_csv(filename)
print(f"\n✅ Saved to {filename}")
