import pandas as pd
import os

print("\n" + "=" * 60)
print("LOADING 1M MASTER DATA")
print("=" * 60)

df = pd.read_csv(
    "data/raw/nifty_1m_master.csv"
)

df["datetime"] = pd.to_datetime(
    df["datetime"]
)

df.set_index(
    "datetime",
    inplace=True
)

# ==========================================
# 5 MIN
# ==========================================

df_5m = df.resample("5min").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})

df_5m.dropna(inplace=True)

# ==========================================
# 15 MIN
# ==========================================

df_15m = df.resample("15min").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})

df_15m.dropna(inplace=True)

# ==========================================
# SAVE
# ==========================================

os.makedirs(
    "data/processed",
    exist_ok=True
)

df_5m.to_csv(
    "data/processed/nifty_5m_master.csv"
)

df_15m.to_csv(
    "data/processed/nifty_15m_master.csv"
)

print("\n" + "=" * 60)
print("RESAMPLING COMPLETE")
print("=" * 60)

print("1M Rows :", len(df))
print("5M Rows :", len(df_5m))
print("15M Rows:", len(df_15m))

print("\nSaved:")
print("data/processed/nifty_5m_master.csv")
print("data/processed/nifty_15m_master.csv")