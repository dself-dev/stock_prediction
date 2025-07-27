import pandas as pd
import ta

# Read the CSV file
df = pd.read_csv('CSV/IONQ_1d_with_rsi.csv')

# Calculate Bollinger Bands using ta library
# Using Close price for calculation (standard 20-period, 2 standard deviations)
bollinger_upper = ta.volatility.bollinger_hband(df['Close'], window=20, window_dev=2)
bollinger_middle = ta.volatility.bollinger_mavg(df['Close'], window=20)  # This is the SMA
bollinger_lower = ta.volatility.bollinger_lband(df['Close'], window=20, window_dev=2)

# Create a new dataframe with only Bollinger Bands
bollinger_df = pd.DataFrame({
    'Bollinger_Upper': bollinger_upper,
    'Bollinger_Middle': bollinger_middle,
    'Bollinger_Lower': bollinger_lower
})

# Save to CSV file
bollinger_df.to_csv('bollinger_bands.csv', index=False)

print("Bollinger Bands saved to bollinger_bands.csv")
print(f"Shape: {bollinger_df.shape}")
print("\nFirst 10 rows:")
print(bollinger_df.head(30))