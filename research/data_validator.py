import pandas as pd

df = pd.read_csv(
    "data/raw/nifty_1m_master.csv"
)

df["datetime"] = pd.to_datetime(
    df["datetime"]
)

print("\n" + "=" * 60)
print("DATA VALIDATION")
print("=" * 60)

print(
    "Rows:",
    len(df)
)

print(
    "Duplicate Timestamps:",
    df["datetime"].duplicated().sum()
)

print(
    "Missing Opens:",
    df["open"].isna().sum()
)

print(
    "Missing Highs:",
    df["high"].isna().sum()
)

print(
    "Missing Lows:",
    df["low"].isna().sum()
)

print(
    "Missing Closes:",
    df["close"].isna().sum()
)

print(
    "Missing Volumes:",
    df["volume"].isna().sum()
)

print(
    "\nStart:",
    df["datetime"].min()
)

print(
    "End:",
    df["datetime"].max()
)