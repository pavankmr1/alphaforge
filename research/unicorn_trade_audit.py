import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN TRADE AUDIT")
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
# COMPONENTS
# ============================================================

sweep = data["SWEEP_SWING_LOW"]
mss = data["BOS_BULLISH"]
quality_fvg = data["QUALITY_BULLISH_FVG"]

# ============================================================
# BUILD ENTRIES
# ============================================================

entries = pd.Series(
    False,
    index=data.index
)

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

        candle_low = data[
            "Low"
        ].iloc[j]

        candle_close = data[
            "Close"
        ].iloc[j]

        candle_open = data[
            "Open"
        ].iloc[j]

        inside_zone = (

            candle_low <= fvg_top

            and

            candle_low >= fvg_bottom

        )

        bullish_close = (
            candle_close >
            candle_open
        )

        if (
            inside_zone
            and
            bullish_close
        ):

            entries.iloc[j] = True
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

# ============================================================
# TRADES
# ============================================================

trades = (
    portfolio
    .trades
    .records_readable
)

# ============================================================
# HOLDING TIMES
# ============================================================

holding_times = (

    trades["Exit Timestamp"]

    -

    trades["Entry Timestamp"]

)

winner_mask = (
    trades["Return"] > 0
)

loser_mask = (
    trades["Return"] <= 0
)

# ============================================================
# REPORT
# ============================================================

print()

print(
    "Trades:",
    len(trades)
)

print()

print("=" * 80)
print("HOLDING TIME STATS")
print("=" * 80)

print(
    "Average Holding:",
    holding_times.mean()
)

print(
    "Median Holding:",
    holding_times.median()
)

print(
    "Shortest Trade:",
    holding_times.min()
)

print(
    "Longest Trade:",
    holding_times.max()
)

print()

print("=" * 80)
print("WINNER HOLDING TIMES")
print("=" * 80)

if winner_mask.sum():

    print(
        "Winner Count:",
        int(winner_mask.sum())
    )

    print(
        "Average Winner Duration:",
        holding_times[
            winner_mask
        ].mean()
    )

    print(
        "Median Winner Duration:",
        holding_times[
            winner_mask
        ].median()
    )

print()

print("=" * 80)
print("LOSER HOLDING TIMES")
print("=" * 80)

if loser_mask.sum():

    print(
        "Loser Count:",
        int(loser_mask.sum())
    )

    print(
        "Average Loser Duration:",
        holding_times[
            loser_mask
        ].mean()
    )

    print(
        "Median Loser Duration:",
        holding_times[
            loser_mask
        ].median()
    )

print()

print("=" * 80)
print("TOP 10 LONGEST TRADES")
print("=" * 80)

longest = trades.copy()

longest["Duration"] = holding_times

print(

    longest

    .sort_values(
        "Duration",
        ascending=False
    )

    [[
        "Entry Timestamp",
        "Exit Timestamp",
        "Return",
        "Duration"
    ]]

    .head(10)

)

print()

print("=" * 80)
print("TOP 10 BEST TRADES")
print("=" * 80)

best = trades.copy()

print(

    best

    .sort_values(
        "Return",
        ascending=False
    )

    [[
        "Entry Timestamp",
        "Exit Timestamp",
        "Return"
    ]]

    .head(10)

)