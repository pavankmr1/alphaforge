import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN BACKTEST")
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
# BUILD RETEST ENTRIES
# ============================================================

entries = pd.Series(
    False,
    index=data.index
)

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    # ---------------------------------------
    # MSS within next 5 candles
    # ---------------------------------------

    mss_window = mss.iloc[
        i:i+6
    ]

    if not mss_window.any():
        continue

    mss_idx = mss_window.idxmax()

    mss_pos = data.index.get_loc(
        mss_idx
    )

    # ---------------------------------------
    # Quality FVG within next 5 candles
    # ---------------------------------------

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window.idxmax()

    fvg_pos = data.index.get_loc(
        fvg_idx
    )

    fvg_top = data[
        "BullishFVG_Top"
    ].iloc[fvg_pos]

    fvg_bottom = data[
        "BullishFVG_Bottom"
    ].iloc[fvg_pos]

    # ---------------------------------------
    # Retest within next 10 candles
    # ---------------------------------------

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
# EXIT
# ============================================================

exits = data["BOS_BEARISH"]

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
# REPORT
# ============================================================

print()

print(
    "Signals:",
    int(entries.sum())
)

print(
    "Trades:",
    portfolio.trades.count()
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
            portfolio.trades.win_rate()
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
            portfolio.trades.profit_factor()
        ),
        4
    )
)

print(
    "Average Winner:",
    round(
        float(
            portfolio.trades.winning.returns.mean()
        ),
        4
    )
)

print(
    "Average Loser:",
    round(
        float(
            portfolio.trades.losing.returns.mean()
        ),
        4
    )
)

print("\n" + "=" * 80)
print("TRADES")
print("=" * 80)

print(
    portfolio.trades.records_readable.head(20)
)