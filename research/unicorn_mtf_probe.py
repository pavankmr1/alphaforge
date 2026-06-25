import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN MTF PROBE")
print("=" * 80)

# ============================================================
# LOAD 1M
# ============================================================

df_1m = pd.read_csv(
    "data/raw/nifty_1m_master.csv"
)

df_1m["datetime"] = pd.to_datetime(
    df_1m["datetime"]
)

df_1m.set_index(
    "datetime",
    inplace=True
)

df_1m.rename(
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
# LOAD 5M
# ============================================================

df_5m = pd.read_csv(
    "data/processed/nifty_5m_master.csv"
)

df_5m["datetime"] = pd.to_datetime(
    df_5m["datetime"]
)

df_5m.set_index(
    "datetime",
    inplace=True
)

df_5m.rename(
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

print("\nComputing Features...")

df_1m = compute_features(df_1m)

df_5m = compute_features(df_5m)

# ============================================================
# FIND FIRST QUALITY 5M FVG
# ============================================================

fvg_rows = df_5m[
    df_5m["QUALITY_BULLISH_FVG"]
]

if len(fvg_rows) == 0:

    print("No 5M Quality FVG Found")
    exit()

fvg_time = fvg_rows.index[0]

print("\n" + "=" * 80)
print("FIRST 5M QUALITY FVG")
print("=" * 80)

print("Time:", fvg_time)

print(
    "Top:",
    fvg_rows.iloc[0]["BullishFVG_Top"]
)

print(
    "Bottom:",
    fvg_rows.iloc[0]["BullishFVG_Bottom"]
)

print(
    "Gap:",
    fvg_rows.iloc[0]["BullishFVG_Gap"]
)

print(
    "GapATR:",
    round(
        fvg_rows.iloc[0]["BullishFVG_GapATR"],
        3
    )
)

# ============================================================
# GET 1M CANDLES INSIDE THIS 5M WINDOW
# ============================================================

window_start = fvg_time

window_end = (
    fvg_time
    +
    pd.Timedelta(minutes=5)
)

candles_1m = df_1m.loc[
    window_start:window_end
]

print("\n" + "=" * 80)
print("1M CANDLES INSIDE 5M FVG WINDOW")
print("=" * 80)

print(
    candles_1m[
        [
            "Open",
            "High",
            "Low",
            "Close"
        ]
    ]
)

# ============================================================
# FIND 1M FVGs INSIDE SAME WINDOW
# ============================================================

fvg_1m = candles_1m[
    candles_1m["BullishFVG"]
]

print("\n" + "=" * 80)
print("1M FVGs INSIDE WINDOW")
print("=" * 80)

if len(fvg_1m) == 0:

    print("NO 1M FVG FOUND")

else:

    print(
        fvg_1m[
            [
                "BullishFVG_Top",
                "BullishFVG_Bottom",
                "BullishFVG_Gap",
                "BullishFVG_GapATR"
            ]
        ]
    )

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(
    "5M FVG Time:",
    fvg_time
)

print(
    "1M Candles:",
    len(candles_1m)
)

print(
    "1M FVG Count:",
    len(fvg_1m)
)