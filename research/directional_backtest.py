from pathlib import Path
import json

import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.dsl_signal_engine_v2 import (
    generate_directional_signals
)

from backtesting.portfolio_engine import (
    run_backtest
)

# ==========================================
# LOAD STRATEGY
# ==========================================
STRATEGY_FILE = Path(
    "data/compiled_strategies_v3/EMA Crossover Trading Strategy (1).json"
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
# DIRECTIONAL SIGNALS
# ==========================================
long_entries, long_exits = (
    generate_directional_signals(
        compiled_logic,
        data
    )
)


long_exits = (
    long_exits
    .shift(1)
    .fillna(False)
    .astype(bool)
)

# ==========================================
# BACKTEST
# ==========================================
import vectorbt as vbt

portfolio = vbt.Portfolio.from_signals(
    close=data["Close"].astype(float),
    entries=long_entries,
    exits=long_exits,
    init_cash=100000,
    freq="1D"
)


print(
    "=" * 60
)

print(
    strategy["name"]
)

print(
    "=" * 60
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
    "Max Drawdown:",
    round(
        float(
            portfolio.max_drawdown()
        ),
        4
    )
)