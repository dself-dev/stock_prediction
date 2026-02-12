import yfinance as yf
from datetime import datetime
from typing import Dict

# --------------------------------------
# Fibonacci retracement calculator
# --------------------------------------
FIB_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]


def calculate_fib_levels(high: float, low: float) -> Dict[float, float]:
    """
    Calculate Fibonacci retracement levels between a swing high and swing low.

    Args:
        high (float): The swing high price.
        low (float): The swing low price.

    Returns:
        dict: A dictionary mapping Fibonacci ratios to price levels.
    """
    diff = high - low
    levels = {}

    for lvl in FIB_LEVELS:
        retracement = high - diff * lvl
        levels[lvl] = retracement

    return levels


def main() -> None:
    """
    CLI tool to compute Fibonacci retracement levels for a given
    stock symbol starting from a user-provided buy date.
    """
    symbol = input("Enter symbol (e.g. AAPL, BTC-USD): ").upper().strip()
    buy_date = input("Enter buy date (YYYY-MM-DD): ").strip()

    # Validate date format
    try:
        buy_date_obj = datetime.strptime(buy_date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # Check future date
    if buy_date_obj > datetime.now():
        print("Buy date cannot be in the future.")
        return

    print("\nFetching data, please wait...\n")

    # Download data
    data = yf.download(symbol, start=buy_date, auto_adjust=False)

    # Validate ticker & data
    if data.empty:
        print(f"No data found for '{symbol}'. Check the ticker or date range.")
        return

    # Ensure columns exist
    if "High" not in data.columns or "Low" not in data.columns:
        print("Downloaded data does not contain High/Low columns.")
        return

    # Clean NaN values
    price_data = data[["High", "Low"]].dropna()

    # Check for enough candles
    if len(price_data) < 2:
        print("Not enough price data to compute Fibonacci levels.")
        return

    # Extract numeric swing values
    try:
        swing_high = price_data["High"].max().item()
        swing_low = price_data["Low"].min().item()
    except AttributeError:
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


if __name__ == "__main__":
    main()
