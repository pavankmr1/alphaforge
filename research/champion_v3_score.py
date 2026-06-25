import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
)

from backtesting.scoring_engine import (
    bullish_score
)

# ==================================
# LOAD DATA
# ==================================

print()
print("=" * 80)
print("LOADING DATA")
print("=" * 80)

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
data.columns = [
    "Open",
    "High",
    "Low",
    "Close",
    "Volume"
]
close=data["Close"]

# ==================================
# FEATURES
# ==================================

print()
print("=" * 80)
print("COMPUTING FEATURES")
print("=" * 80)

data = compute_features(data)
context = build_context(data)

score = bullish_score(
    data,
    context
)
# ==================================
# ICT TREND FILTER
# ==================================

# bullish_trend = (

#     data["EMA20"]

#     >

#     data["EMA50"]

# )
bullish_trend = (

    (data["EMA20"] > data["EMA50"])

    &

    (data["EMA50"] > data["EMA200"])

)
# ==================================
# RECENT LIQUIDITY SWEEP
# ==================================

recent_sweep = (

    data["SWEEP_SWING_LOW"]

    .rolling(5)

    .max()

    .fillna(False)

    .astype(bool)

)

# ==================================
# MSS / BOS CONFIRMATION
# ==================================

bullish_mss = (

    data["BOS_BULLISH"]

)

# ==================================
# ENTRY
# ==================================

entries = (

    bullish_trend

    &

    recent_sweep

    &

    bullish_mss

    &

    (score >= 8)

)
# ==================================
# EXIT
# ==================================

exits = (

    data["BOS_BEARISH"]

)

# ==================================
# BACKTEST
# ==================================

portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=entries,

    exits=exits,

    init_cash=100000,

    freq="15m"

)

# ==================================
# TRADE METRICS
# ==================================

trades = portfolio.trades.records_readable


print()
print("=" * 80)
print("FILTER COUNTS")
print("=" * 80)

print("Bullish Trend:", bullish_trend.sum())
print("Recent Sweep:", recent_sweep.sum())
print("Bullish MSS:", bullish_mss.sum())
print("Score >= 8:", (score >= 8).sum())
print("Final Entries:", entries.sum())


returns = trades["Return"]

winners = returns[
    returns > 0
]

losers = returns[
    returns < 0
]

profit_factor = (

    winners.sum()

    /

    abs(losers.sum())

    if len(losers) > 0

    else float("inf")

)

# ==================================
# REPORT
# ==================================

print()
print("=" * 80)
print("ICT SWEEP + MSS")
print("=" * 80)

print(
    "Signals:",
    int(entries.sum())
)

print(
    "Trades:",
    len(trades)
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
            profit_factor
        ),
        4
    )
)

if len(winners) > 0:

    print(
        "Average Winner:",
        round(
            float(
                winners.mean()
            ),
            4
        )
    )

if len(losers) > 0:

    print(
        "Average Loser:",
        round(
            float(
                losers.mean()
            ),
            4
        )
    )