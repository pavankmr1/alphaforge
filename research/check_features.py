import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

df = pd.read_csv(
    "data/processed/nifty_15m_master.csv"
)

df["datetime"] = pd.to_datetime(
    df["datetime"]
)

df.set_index(
    "datetime",
    inplace=True
)

# ==========================================
# RENAME FOR FEATURE ENGINE
# ==========================================

df.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    },
    inplace=True
)

df = compute_features(df)

print("\nFEATURES")
print("=" * 80)

for col in sorted(df.columns):
    print(col)