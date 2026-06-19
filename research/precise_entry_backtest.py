import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

# ==================================
# DATA
# ==================================

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

# ==================================
# TREND
# ==================================

trend = (

    data["EMA20"]

    >

    data["EMA50"]

)

# ==================================
# REACTION ZONE
# ==================================

reaction_zone = (

    data["Low"]

    <=

    data["PREV_BEARISH_HIGH"]

)

# ==================================
# LIQUIDITY SWEEP
# ==================================

liquidity_sweep = (

    data["Low"]

    <

    data["LiquidityLow"].shift(1)

)

# ==================================
# CONFIRMATION
# ==================================

confirmation = (

    data["BULLISH_CONFIRMATION"]

)

# ==================================
# ENTRY
# ==================================

entries = (

    trend

    &

    reaction_zone

    &

    liquidity_sweep

    &

    confirmation

)

entries = (
    entries
    .fillna(False)
    .astype(bool)
)

# ==================================
# EXIT
# ==================================

exits = (

    data["BEARISH_CONFIRMATION"]

)

exits = (
    exits
    .shift(1)
    .fillna(False)
    .astype(bool)
)

# ==================================
# BACKTEST
# ==================================

portfolio = vbt.Portfolio.from_signals(
    close=data["Close"].astype(float),
    entries=entries,
    exits=exits,
    init_cash=100000,
    freq="1D"
)

print()
print("=" * 60)
print("PRECISE ENTRY PROTOTYPE")
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
        float(portfolio.total_return()),
        4
    )
)

print(
    "Sharpe:",
    round(
        float(portfolio.sharpe_ratio()),
        4
    )
)

print(
    "Win Rate:",
    round(
        float(portfolio.trades.win_rate()),
        4
    )
)

print(
    "Max DD:",
    round(
        float(portfolio.max_drawdown()),
        4
    )
)

print()

print(
    "Trend:",
    int(trend.sum())
)

print(
    "Reaction Zone:",
    int(reaction_zone.sum())
)

print(
    "Liquidity Sweep:",
    int(liquidity_sweep.sum())
)

print(
    "Confirmation:",
    int(confirmation.sum())
)

print(
    "Final Entries:",
    int(entries.sum())
)