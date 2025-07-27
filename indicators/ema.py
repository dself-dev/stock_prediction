import pandas as pd
import ta

# Read the CSV file
df = pd.read_csv('CSV/IONQ_1d_with_rsi.csv')

# Calculate EMAs using ta library
# Standard periods: 12 and 26 (commonly used for MACD)
ema_12 = ta.trend.ema_indicator(df['Close'], window=12)
ema_26 = ta.trend.ema_indicator(df['Close'], window=26)

# Create a new dataframe with only EMAs
ema_df = pd.DataFrame({
    'EMA_12': ema_12,
    'EMA_26': ema_26
})

# Save to CSV file
ema_df.to_csv('ema_indicators.csv', index=False)

print("EMA indicators saved to ema_indicators.csv")
print(f"Shape: {ema_df.shape}")
print("\nFirst 30 rows:")
print(ema_df.head(30))