import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN RETEST TEST")
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
# UNICORN SETUPS
# ============================================================

unicorn_setup = pd.Series(
    False,
    index=data.index
)

retest_signal = pd.Series(
    False,
    index=data.index
)

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    # ----------------------------------
    # MSS within next 5 candles
    # ----------------------------------

    mss_window = mss.iloc[
        i:i+6
    ]

    if not mss_window.any():
        continue

    mss_idx = mss_window.idxmax()

    mss_pos = data.index.get_loc(
        mss_idx
    )

    # ----------------------------------
    # QUALITY FVG within next 5 candles
    # ----------------------------------

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window.idxmax()

    fvg_pos = data.index.get_loc(
        fvg_idx
    )

    unicorn_setup.iloc[
        fvg_pos
    ] = True

    # ----------------------------------
    # FVG ZONE
    # ----------------------------------

    fvg_top = data[
        "BullishFVG_Top"
    ].iloc[fvg_pos]

    fvg_bottom = data[
        "BullishFVG_Bottom"
    ].iloc[fvg_pos]

    # ----------------------------------
    # RETEST LOOKAHEAD
    # ----------------------------------

    for j in range(
        fvg_pos + 1,
        min(
            fvg_pos + 11,
            len(data)
        )
    ):

        candle_low = data[
            "Low"
        ].iloc[j]

        candle_close = data[
            "Close"
        ].iloc[j]

        # Price enters FVG

        inside_zone = (

            candle_low
            <=
            fvg_top

            and

            candle_low
            >=
            fvg_bottom

        )

        bullish_close = (

            candle_close
            >
            data["Open"].iloc[j]

        )

        if (
            inside_zone
            and
            bullish_close
        ):

            retest_signal.iloc[
                j
            ] = True

            break

# ============================================================
# REPORT
# ============================================================

print()

print(
    "Quality Unicorn Setups:",
    int(
        unicorn_setup.sum()
    )
)

print(
    "Retest Signals:",
    int(
        retest_signal.sum()
    )
)

print()

print(
    retest_signal[
        retest_signal
    ].head(20)
)