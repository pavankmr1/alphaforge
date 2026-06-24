import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("QUALITY FVG ANALYSIS")
print("=" * 80)

# ============================================================
# LOAD
# ============================================================

data = pd.read_csv(
    "data/processed/nifty_15m_master.csv"
)

data["datetime"] = pd.to_datetime(
    data["datetime"]
)

data.set_index(
    "datetime",
    inplace=True
)

data.rename(
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

data = compute_features(data)

# ============================================================
# GAP SIZE
# ============================================================

gap_size = pd.Series(
    0.0,
    index=data.index
)

gap_ratio = pd.Series(
    0.0,
    index=data.index
)

for i in range(2, len(data)):

    if not data["BullishFVG"].iloc[i]:
        continue

    c1_high = data["High"].iloc[i - 2]
    c3_low = data["Low"].iloc[i]

    gap = c3_low - c1_high

    atr = data["ATR14"].iloc[i]

    gap_size.iloc[i] = gap

    if atr > 0:
        gap_ratio.iloc[i] = gap / atr

# ============================================================
# QUALITY FVG
# ============================================================

quality_fvg = (

    data["BullishFVG"]

    &

    (gap_ratio >= 0.25)

    &

    (gap_ratio <= 2.0)

)

# ============================================================
# REPORT
# ============================================================

print()

print(
    "Total Bullish FVG:",
    int(data["BullishFVG"].sum())
)

print(
    "Quality Bullish FVG:",
    int(quality_fvg.sum())
)

print(
    "Retained %",
    round(
        quality_fvg.sum()
        /
        data["BullishFVG"].sum()
        * 100,
        2
    )
)

print()

print(
    "Average Quality Gap:",
    round(
        gap_size[
            quality_fvg
        ].mean(),
        2
    )
)

print(
    "Average Quality Gap/ATR:",
    round(
        gap_ratio[
            quality_fvg
        ].mean(),
        2
    )
)