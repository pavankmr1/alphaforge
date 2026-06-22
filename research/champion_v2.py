import yfinance as yf
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
# STRICT CONTEXT
# ==================================

entries = (

    (score >= 8)

    &

    recent_sweep

    &

    context["BULLISH_CONTEXT"]

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
# REPORT
# ==================================

print()
print("=" * 60)
print("ALPHAFORGE CHAMPION V2")
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