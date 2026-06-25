import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN WINNER ANALYSIS")
print("=" * 80)

# ============================================================
# LOAD DATA
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
# BUILD UNICORN ENTRIES
# ============================================================

entries = pd.Series(
    False,
    index=data.index
)

entry_features = {}

sweep = data["SWEEP_SWING_LOW"]
mss = data["BOS_BULLISH"]
quality_fvg = data["QUALITY_BULLISH_FVG"]

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    mss_window = mss.iloc[
        i:i+6
    ]

    if not mss_window.any():
        continue

    mss_idx = mss_window[
        mss_window
    ].index[0]

    mss_pos = data.index.get_loc(
        mss_idx
    )

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window[
        fvg_window
    ].index[0]

    fvg_pos = data.index.get_loc(
        fvg_idx
    )

    fvg_top = data[
        "BullishFVG_Top"
    ].iloc[fvg_pos]

    fvg_bottom = data[
        "BullishFVG_Bottom"
    ].iloc[fvg_pos]

    for j in range(
        fvg_pos + 1,
        min(
            fvg_pos + 11,
            len(data)
        )
    ):

        inside_zone = (

            data["Low"].iloc[j]
            <=
            fvg_top

            and

            data["Low"].iloc[j]
            >=
            fvg_bottom

        )

        bullish_close = (

            data["Close"].iloc[j]
            >
            data["Open"].iloc[j]

        )

        if (
            inside_zone
            and
            bullish_close
        ):

            entries.iloc[j] = True

            entry_features[
                data.index[j]
            ] = {

                "GapATR":
                    data[
                        "BullishFVG_GapATR"
                    ].iloc[fvg_pos],

                "Gap":
                    data[
                        "BullishFVG_Gap"
                    ].iloc[fvg_pos],

                "ATR":
                    data[
                        "ATR14"
                    ].iloc[j],

                "RSI":
                    data[
                        "RSI14"
                    ].iloc[j],

                "VolumeRatio":
                    (
                        data["Volume"].iloc[j]
                        /
                        max(
                            data["VOL_MA20"].iloc[j],
                            1
                        )
                    ),

                "Trend":
                    bool(
                        data[
                            "BULLISH_TREND_V2"
                        ].iloc[j]
                    ),

                "Hour":
                    data.index[j].hour

            }

            break

# ============================================================
# EXITS
# ============================================================

exits = data[
    "BOS_BEARISH"
]

# ============================================================
# BACKTEST
# ============================================================

portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=entries,

    exits=exits,

    init_cash=100000,

    freq="15m"
)

trades = (
    portfolio
    .trades
    .records_readable
)

# ============================================================
# BUILD ANALYSIS DATASET
# ============================================================

analysis_rows = []

for _, trade in trades.iterrows():

    entry_time = trade[
        "Entry Timestamp"
    ]

    if entry_time not in entry_features:
        continue

    feat = entry_features[
        entry_time
    ]

    analysis_rows.append({

        "Return":
            trade["Return"],

        "Winner":
            trade["Return"] > 0,

        **feat

    })

analysis_df = pd.DataFrame(
    analysis_rows
)

# ============================================================
# SPLIT
# ============================================================

winners = analysis_df[
    analysis_df["Winner"]
]

losers = analysis_df[
    ~analysis_df["Winner"]
]

# ============================================================
# REPORT
# ============================================================

print()

print("=" * 80)
print("TRADE COUNTS")
print("=" * 80)

print(
    "Total:",
    len(analysis_df)
)

print(
    "Winners:",
    len(winners)
)

print(
    "Losers:",
    len(losers)
)

# ============================================================
# WINNERS
# ============================================================

print()
print("=" * 80)
print("WINNERS")
print("=" * 80)

print(
    winners[
        [
            "GapATR",
            "Gap",
            "ATR",
            "RSI",
            "VolumeRatio"
        ]
    ]
    .mean()
)

# ============================================================
# LOSERS
# ============================================================

print()
print("=" * 80)
print("LOSERS")
print("=" * 80)

print(
    losers[
        [
            "GapATR",
            "Gap",
            "ATR",
            "RSI",
            "VolumeRatio"
        ]
    ]
    .mean()
)

# ============================================================
# TOP WINNERS
# ============================================================

print()
print("=" * 80)
print("TOP 10 WINNERS")
print("=" * 80)

print(

    analysis_df

    .sort_values(
        "Return",
        ascending=False
    )

    .head(10)

)

# ============================================================
# TOP LOSERS
# ============================================================

print()
print("=" * 80)
print("TOP 10 LOSERS")
print("=" * 80)

print(

    analysis_df

    .sort_values(
        "Return",
        ascending=True
    )

    .head(10)

)