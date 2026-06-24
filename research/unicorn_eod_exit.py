import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN EOD EXIT BACKTEST")
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

print("\n" + "=" * 80)
print("COMPUTING FEATURES")
print("=" * 80)

data = compute_features(data)

# ============================================================
# COMPONENTS
# ============================================================

sweep = data["SWEEP_SWING_LOW"]

mss = data["BOS_BULLISH"]

quality_fvg = data["QUALITY_BULLISH_FVG"]

# ============================================================
# BUILD UNICORN ENTRIES
# ============================================================

entries = pd.Series(
    False,
    index=data.index
)

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    # ----------------------------------------------------
    # MSS
    # ----------------------------------------------------

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

    # ----------------------------------------------------
    # QUALITY FVG
    # ----------------------------------------------------

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

    # ----------------------------------------------------
    # RETEST
    # ----------------------------------------------------

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

        candle_open = data[
            "Open"
        ].iloc[j]

        candle_close = data[
            "Close"
        ].iloc[j]

        inside_zone = (

            candle_low <= fvg_top

            and

            candle_low >= fvg_bottom

        )

        bullish_close = (

            candle_close
            >
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
# BOS EXIT
# ============================================================

bos_exit = data[
    "BOS_BEARISH"
]

# ============================================================
# EOD EXIT (3:15 PM)
# ============================================================

eod_exit = (
    (data.index.hour == 9)
    &
    (data.index.minute == 45)
)
print("EOD EXIT COUNT:", int(eod_exit.sum()))
# ============================================================
# FINAL EXITS
# ============================================================

exits = (

    bos_exit

    |

    eod_exit

)

# ============================================================
# BACKTEST
# ============================================================

print("\n" + "=" * 80)
print("RUNNING BACKTEST")
print("=" * 80)

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

trades = portfolio.trades

# ============================================================
# REPORT
# ============================================================

print()

print("=" * 80)
print("UNICORN EOD EXIT RESULTS")
print("=" * 80)

print(
    "Signals:",
    int(entries.sum())
)

print(
    "Trades:",
    trades.count()
)

print(
    "Return:",
    round(
        float(
            portfolio.total_return()
        ),
        4
    )
)

print(
    "Sharpe:",
    round(
        float(
            portfolio.sharpe_ratio()
        ),
        4
    )
)

print(
    "Win Rate:",
    round(
        float(
            trades.win_rate()
        ),
        4
    )
)

print(
    "Max DD:",
    round(
        float(
            portfolio.max_drawdown()
        ),
        4
    )
)

print(
    "Profit Factor:",
    round(
        float(
            trades.profit_factor()
        ),
        4
    )
)

print(
    "Average Winner:",
    round(
        float(
            trades.winning.returns.mean()
        ),
        4
    )
)

print(
    "Average Loser:",
    round(
        float(
            trades.losing.returns.mean()
        ),
        4
    )
)

print()

print("=" * 80)
print("COMPARISON")
print("=" * 80)

print("Original Unicorn")
print("Return        : 8.16%")
print("Profit Factor : 1.76")
print("Sharpe        : 2.94")
print()

print("EOD Unicorn")
print(
    "Return        :",
    round(
        float(
            portfolio.total_return() * 100
        ),
        2
    ),
    "%"
)
print(
    "Profit Factor :",
    round(
        float(
            trades.profit_factor()
        ),
        2
    )
)
print(
    "Sharpe        :",
    round(
        float(
            portfolio.sharpe_ratio()
        ),
        2
    )
)
print("\nFIRST 20 TIMESTAMPS")
print(data.index[:20])

print("\nLAST 20 TIMESTAMPS")
print(data.index[-20:])
print("\nEOD EXIT COUNT")
print(int(eod_exit.sum()))

print("\nEOD EXIT CANDLES")
print(data[eod_exit].head())