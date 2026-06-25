import yfinance as yf
import vectorbt as vbt
import pandas as pd

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
# DATA
# ==================================

data = yf.download(
    "^NSEI",
    period="60d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

context = build_context(data)

score = bullish_score(
    data,
    context
)

# ==================================
# ENTRY
# ==================================

recent_sweep = (

    data["SWEEP_SWING_LOW"]
    .rolling(5)
    .max()
    .fillna(False)
    .astype(bool)

)

entries = (

    (score >= 8)

    &
    recent_sweep

)

# ==================================
# ATR RR EXIT
# ==================================

exits = pd.Series(
    False,
    index=data.index
)

in_trade = False
stop_price = None
target_price = None

for i in range(len(data)):

    if entries.iloc[i] and not in_trade:

        entry_price = (
            data["Close"].iloc[i]
        )

        atr = (
            data["ATR14"].iloc[i]
        )

        stop_price = (
            entry_price
            -
            2 * atr
        )

        target_price = (
            entry_price
            +
            4 * atr
        )

        in_trade = True

    elif in_trade:

        low = data["Low"].iloc[i]
        high = data["High"].iloc[i]

        stop_hit = (
            low <= stop_price
        )

        target_hit = (
            high >= target_price
        )

        if stop_hit or target_hit:

            exits.iloc[i] = True

            in_trade = False

            stop_price = None
            target_price = None

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
# REPORT
# ==================================

print()
print("=" * 60)
print("ATR RR EXIT TEST")
print("=" * 60)

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