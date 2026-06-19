from pathlib import Path
import json

import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

from backtesting.dsl_executor import (
    execute_rule
)

# ==========================================
# LOAD STRATEGY
# ==========================================

STRATEGY_FILE = Path(
    "data/compiled_strategies_v3/9&20EMA STRATEGY.json"
)

strategy = json.loads(
    STRATEGY_FILE.read_text()
)

compiled_logic = strategy.get(
    "compiled_entry_logic",
    []
)

# ==========================================
# MARKET DATA
# ==========================================

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(
    data
)

# ==========================================
# BUILD SIGNALS
# ==========================================

cross_above = None
cross_below = None
trend_up = None

for item in compiled_logic:

    dsl = item.get(
        "dsl"
    )

    if not dsl:
        continue

    for rule in dsl.get(
        "rules",
        []
    ):

        signal = execute_rule(
            rule,
            data
        )

        if signal is None:
            continue

        signal = (
            signal
            .fillna(False)
            .astype(bool)
        )

        rule_type = rule.get(
            "type"
        )

        if rule_type == "cross_above":

            cross_above = signal

        elif rule_type == "cross_below":

            cross_below = signal

        elif rule_type == "trend_up":

            trend_up = signal

# ==========================================
# ENTRY + FILTER LOGIC
# ==========================================

entries = (
    cross_above
    &
    trend_up
)

exits = (
    cross_below
    .shift(1)
    .fillna(False)
)
entries = (
    entries
    .fillna(False)
    .astype(bool)
)

exits = (
    exits
    .fillna(False)
    .astype(bool)
)

close = (
    data["Close"]
    .astype(float)
)
# ==========================================
# REPORT
# ==========================================

print()
print(
    "Cross Above:",
    int(cross_above.sum())
)

print(
    "Trend Up:",
    int(trend_up.sum())
)

print(
    "Cross Below:",
    int(cross_below.sum())
)

print(
    "Final Entries:",
    int(entries.sum())
)

print(
    "Final Exits:",
    int(exits.sum())
)

# ==========================================
# BACKTEST
# ==========================================
print(type(entries))
print(type(exits))

print(entries.dtype)
print(exits.dtype)

print(type(data["Close"]))
print(data["Close"].dtype)

print(entries.head())
print(exits.head())
portfolio = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    init_cash=100000,
    freq="1D"
)

print()
print("=" * 60)
print(strategy["name"])
print("=" * 60)

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
    "Max Drawdown:",
    round(
        float(
            portfolio.max_drawdown()
        ),
        4
    )
)