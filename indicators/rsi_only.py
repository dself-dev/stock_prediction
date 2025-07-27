import pandas as pd
from ta.momentum import RSIIndicator

# Ask for CSV file
file_path = input("Enter the CSV filename (e.g. AAPL_1d.csv): ")

# Load the CSV and parse dates
df = pd.read_csv(file_path, index_col=0, parse_dates=True)

# Ensure 'Close' column exists
if "Close" not in df.columns:
    print("❌ 'Close' column not found.")
    exit()

# Convert 'Close' to numeric in case it's stored as string
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

# Drop rows with invalid or missing 'Close' values
df = df.dropna(subset=["Close"])

# Compute RSI (14-period)
rsi_calc = RSIIndicator(close=df["Close"], window=14)
df["RSI_14"] = rsi_calc.rsi()

# Make a new DataFrame with only the RSI_14 column
df_rsi = df[["RSI_14"]].copy()

# Preview and save
print(df_rsi.tail())

# Save to a new CSV (e.g., AAPL_1d_rsi.csv)
out_file = file_path.replace(".csv", "_rsi.csv")
df_rsi.to_csv(out_file)
print(f"\n✅ RSI-only file saved as {out_file}")
