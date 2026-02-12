import yfinance as yf
import pandas as pd
from pathlib import Path

def download_stock_data():
    # --- USER INPUT ---
    ticker = input("Enter stock ticker (ex: AAPL): ").upper()

    print("\nEnter START date:")
    start_year = input("Year (YYYY): ")
    start_month = input("Month (MM): ")
    start_day = input("Day (DD): ")

    print("\nEnter END date:")
    end_year = input("Year (YYYY): ")
    end_month = input("Month (MM): ")
    end_day = input("Day (DD): ")

    start_date = f"{start_year}-{start_month}-{start_day}"
    end_date = f"{end_year}-{end_month}-{end_day}"

    # --- DOWNLOAD DATA ---
    print(f"\nDownloading {ticker} from {start_date} to {end_date}...")
    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=False
    )

    # --- FIX MULTIINDEX COLUMNS ---
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # --- CHECK EMPTY ---
    if df.empty:
        print("\nERROR: No data returned. Change end date.")
        return

    print("\nDownloaded data preview:")
    print(df.head())

    # --- REQUIRED COLUMNS ---
    required_cols = ["Open", "High", "Low", "Close", "Volume"]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print("\nERROR: Missing columns:", missing)
        print("Columns returned:", df.columns)
        return

    # --- SLICE ---
    df = df[required_cols]

    # --- CLEAN NUMERIC ---
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --- SAVE ---
    save_dir = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv")
    save_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{ticker}_{start_date}_to_{end_date}.csv"
    full_path = save_dir / file_name

    df.to_csv(full_path, index=True)

    print(f"\nSaved CSV to:\n{full_path}")
    print(df.head())


if __name__ == "__main__":
    download_stock_data()
