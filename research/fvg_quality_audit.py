import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("FVG QUALITY AUDIT")
print("=" * 80)

# ============================================================
# LOAD DATA
# ============================================================

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

# ============================================================
# FEATURES
# ============================================================

df = compute_features(df)

# ============================================================
# FIND BULLISH FVGs
# ============================================================

records = []

for i in range(2, len(df)):

    if not df["BullishFVG"].iloc[i]:
        continue

    candle1_high = df["High"].iloc[i - 2]
    candle3_low = df["Low"].iloc[i]

    gap_size = (
        candle3_low
        -
        candle1_high
    )

    atr = df["ATR14"].iloc[i]

    atr_ratio = (
        gap_size / atr
        if atr > 0
        else 0
    )

    records.append({

        "datetime":
            df.index[i],

        "gap_size":
            round(gap_size, 2),

        "atr":
            round(atr, 2),

        "atr_ratio":
            round(atr_ratio, 3)

    })

audit = pd.DataFrame(
    records
)

print(
    "\nTotal Bullish FVGs:",
    len(audit)
)

print(
    "\nAverage Gap:",
    round(
        audit["gap_size"].mean(),
        2
    )
)

print(
    "Median Gap:",
    round(
        audit["gap_size"].median(),
        2
    )
)

print(
    "Max Gap:",
    round(
        audit["gap_size"].max(),
        2
    )
)

print(
    "Min Gap:",
    round(
        audit["gap_size"].min(),
        2
    )
)

print(
    "\nAverage Gap / ATR:",
    round(
        audit["atr_ratio"].mean(),
        3
    )
)

print(
    "Median Gap / ATR:",
    round(
        audit["atr_ratio"].median(),
        3
    )
)

print("\n" + "=" * 80)
print("SMALLEST 20 FVGs")
print("=" * 80)

print(
    audit
    .sort_values("gap_size")
    .head(20)
)

print("\n" + "=" * 80)
print("LARGEST 20 FVGs")
print("=" * 80)

print(
    audit
    .sort_values(
        "gap_size",
        ascending=False
    )
    .head(20)
)