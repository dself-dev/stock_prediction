import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from services.indicator_engine import apply_indicators

from main.predictions.predict_tomorrow import TomorrowPredictor


CSV_PATH = r"C:\Users\dself\OneDrive\Market_data\AAPL_1d_complete.csv"


def main():
    # 1. Load CSV
    df = pd.read_csv(CSV_PATH)

    # If Date exists, parse it (safe)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # 2. Apply indicators
    df = apply_indicators(df)

    # 3. Train model
    model = TomorrowPredictor()
    model.train(df)

    # 4. Predict tomorrow
    predicted_close, current_price, change_pct = model.predict(df)

    # 5. Output
    print("=" * 60)
    print("CSV-BASED TRAINING TEST (NO API)")
    print("=" * 60)
    print(f"Current Close:   ${current_price:.2f}")
    print(f"Predicted Close: ${predicted_close:.2f}")
    print(f"Change %:        {change_pct:+.2f}%")
    print("Direction:", "UP" if predicted_close > current_price else "DOWN")
    print("=" * 60)


if __name__ == "__main__":
    main()
