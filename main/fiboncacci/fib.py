
import yfinance as yf
from datetime import datetime

# --------------------------------------
# Fibonacci retracement calculator
# --------------------------------------
FIB_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]


def calculate_fib_levels(high, low):
    # Ensure we're always working with floats
    high = float(high)
    low = float(low)

    diff = high - low
    levels = {}

    for lvl in FIB_LEVELS:
        retracement = high - diff * lvl
        levels[lvl] = retracement

    return levels


# --------------------------------------
# Main Program
# --------------------------------------
def main():
    symbol = input("Enter symbol (e.g. AAPL, BTC-USD): ").upper()
    buy_date = input("Enter buy date (YYYY-MM-DD): ")

    # Validate date format
    try:
        datetime.strptime(buy_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    print("\nFetching data, please wait...\n")

    # Explicitly set auto_adjust to avoid FutureWarning
    data = yf.download(symbol, start=buy_date, auto_adjust=False)

    if data.empty:
        print("No data found. Check symbol or date range.")
        return

    # Make sure High/Low columns exist and have data
    if "High" not in data.columns or "Low" not in data.columns:
        print("Downloaded data does not contain 'High' and 'Low' columns.")
        return

    # Drop any rows where High/Low is NaN
    price_data = data[["High", "Low"]].dropna()

    if price_data.empty:
        print("No valid High/Low data after cleaning. Try a different date range.")
        return

    # Find swing high and swing low from the buy date to now
    swing_high = float(price_data["High"].max())
    swing_low = float(price_data["Low"].min())

    print(f"Swing Low  (from {buy_date}): {swing_low:.2f}")
    print(f"Swing High (from {buy_date}): {swing_high:.2f}\n")

    # Calculate Fibonacci retracement levels
    fibs = calculate_fib_levels(swing_high, swing_low)

    print("Fibonacci Retracement Levels:")
    for lvl, price in fibs.items():
        print(f"  {lvl * 100:.1f}%  ->  {price:.2f}")

    print("\nDone.")


# Run the program
if __name__ == "__main__":
    main()
