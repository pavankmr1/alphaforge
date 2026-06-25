import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

# ============================================================
# LOAD DATA
# ============================================================

print("\n" + "=" * 80)
print("LOADING DATA")
print("=" * 80)

data = pd.read_csv(
    "data/processed/nifty_5m_master.csv"
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

print("\n" + "=" * 80)
print("COMPUTING FEATURES")
print("=" * 80)

data = compute_features(data)

# ============================================================
# STEP 1
# LIQUIDITY SWEEP
# ============================================================

sweep = data["SWEEP_SWING_LOW"]

# ============================================================
# STEP 2
# MSS / BOS
# ============================================================

mss = data["BOS_BULLISH"]

# ============================================================
# STEP 3
# BULLISH FVG
# ============================================================

fvg = data["BullishFVG"]

# ============================================================
# STEP 4
# SWEEP -> MSS SEQUENCE
# MSS must happen within next 5 candles
# ============================================================

sweep_mss = pd.Series(
    False,
    index=data.index
)

for i in range(len(data) - 5):

    if sweep.iloc[i]:

        future_mss = mss.iloc[
            i:i+6
        ].any()

        if future_mss:

            sweep_mss.iloc[i] = True

# ============================================================
# STEP 5
# SWEEP -> MSS -> FVG
# FVG within next 5 candles
# ============================================================

unicorn_setup = pd.Series(
    False,
    index=data.index
)

for i in range(len(data) - 10):

    if sweep.iloc[i]:

        mss_window = mss.iloc[
            i:i+6
        ]

        if not mss_window.any():
            continue

        mss_idx = (
            mss_window.idxmax()
        )

        mss_pos = (
            data.index.get_loc(
                mss_idx
            )
        )

        fvg_window = fvg.iloc[
            mss_pos:mss_pos+6
        ]

        if fvg_window.any():

            unicorn_setup.iloc[
                mss_pos
            ] = True

# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 80)
print("UNICORN COMPONENT ANALYSIS")
print("=" * 80)

print(
    "Total Candles:",
    len(data)
)

print(
    "Liquidity Sweeps:",
    int(sweep.sum())
)

print(
    "Bullish MSS:",
    int(mss.sum())
)

print(
    "Bullish FVG:",
    int(fvg.sum())
)

print(
    "Sweep -> MSS:",
    int(sweep_mss.sum())
)

print(
    "Unicorn Setups:",
    int(unicorn_setup.sum())
)

print("\nFIRST 20 UNICORN SETUPS\n")

print(
    unicorn_setup[
        unicorn_setup
    ].head(20)
)