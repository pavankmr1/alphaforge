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
# LOAD MASTER DATA
# ==================================

print()
print("=" * 80)
print("LOADING 5 YEAR DATA")
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

print(
    "Rows:",
    len(data)
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

# ==================================
# SCORE
# ==================================

score = bullish_score(
    data,
    context
)

# ==================================
# RECENT SWEEP
# ==================================

recent_sweep = (

    data["SWEEP_SWING_LOW"]

    .rolling(5)

    .max()

    .fillna(False)

    .astype(bool)

)

# ==================================
# CHAMPION V2
# ==================================

entries = (

    (score >= 8)

    &

    recent_sweep

    &

    context["BULLISH_CONTEXT"]

)

exits = (

    data["BOS_BEARISH"]

)

# ==================================
# BACKTEST
# ==================================

print()
print("=" * 80)
print("RUNNING BACKTEST")
print("=" * 80)

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

expectancy = returns.mean()

# ==================================
# REPORT
# ==================================

print()
print("=" * 80)
print("ALPHAFORGE CHAMPION V2 - FULL HISTORY")
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

print(
    "Expectancy:",
    round(
        float(
            expectancy
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

print()
print("=" * 80)
print("DATE RANGE")
print("=" * 80)

print(
    "Start:",
    data.index.min()
)

print(
    "End:",
    data.index.max()
)