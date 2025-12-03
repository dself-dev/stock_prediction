# # test_it.py   ← run this to make sure it works
# from pathlib import Path
# import pandas as pd
# from services.indicator_engine import apply_indicators

# # my usual test file – never moving this path
# csv = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")
# df = pd.read_csv(csv, parse_dates=["Date"], index_col="Date")

# # just rsi + bollinger for now – exactly what i asked for
# full_df, latest = apply_indicators(df, use=["rsi", "bollinger"])

# print("\nlatest values (this is the dict i actually care about):")
# for k, v in latest.items():
#     print(f"{k:20} → {v}")

# print(f"\nadded columns: {[c for c in full_df.columns if c not in df.columns]}")
# test_it.py   ← run this to make sure it works
from pathlib import Path
import pandas as pd
from services.indicator_engine import apply_indicators

# my usual test file – never moving this path
csv = Path(r"C:\Users\dself\OneDrive\Market_data\test_csv\AAPL_2022-01-01_to_2025-10-27.csv")
df = pd.read_csv(csv, parse_dates=["Date"], index_col="Date")

# just rsi + bollinger for now – exactly what i asked for
full_df, latest = apply_indicators(df, use=["rsi", "bollinger"])

print("\nlatest values (this is the dict i actually care about):")
for k, v in latest.items():
    print(f"{k:20} → {v}")

print(f"\nadded columns: {[c for c in full_df.columns if c not in df.columns]}")