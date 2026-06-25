import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN V2 COMPONENT ANALYSIS")
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
# COMPONENTS
# ============================================================

sweep = data["SWEEP_SWING_LOW"]

mss = data["BOS_BULLISH"]

quality_fvg = data["QUALITY_BULLISH_FVG"]

# ============================================================
# SWEEP -> MSS -> QUALITY FVG
# ============================================================

unicorn_setup = pd.Series(
    False,
    index=data.index
)

for i in range(len(data) - 10):

    if not sweep.iloc[i]:
        continue

    # MSS within next 5 candles

    mss_window = mss.iloc[
        i:i+6
    ]

    if not mss_window.any():
        continue

    mss_idx = mss_window.idxmax()

    mss_pos = data.index.get_loc(
        mss_idx
    )

    # QUALITY FVG within next 5 candles

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if fvg_window.any():

        unicorn_setup.iloc[
            mss_pos
        ] = True

# ============================================================
# REPORT
# ============================================================

print()

print(
    "Liquidity Sweeps:",
    int(sweep.sum())
)

print(
    "Bullish MSS:",
    int(mss.sum())
)

print(
    "Quality Bullish FVG:",
    int(quality_fvg.sum())
)

print(
    "Unicorn V2 Setups:",
    int(unicorn_setup.sum())
)

print()

print(
    unicorn_setup[
        unicorn_setup
    ].head(20)
)