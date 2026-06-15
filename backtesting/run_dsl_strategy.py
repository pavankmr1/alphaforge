from pathlib import Path

import json
import yfinance as yf

from loguru import logger

from backtesting.feature_engine import (
    compute_features
)

from backtesting.dsl_signal_engine import (
    generate_dsl_signals
)

from backtesting.portfolio_engine import (
    run_backtest
)

from backtesting.metrics_engine import (
    calculate_metrics
)

from backtesting.report_generator import (
    save_report
)

# ==========================================
# LOAD STRATEGY
# ==========================================
strategy_files = list(

    Path(
        "data/compiled_strategies_v2"
    ).glob("*.json")
)

if len(strategy_files) == 0:

    raise ValueError(
        "No compiled strategies found."
    )

# ==========================================
# PICK STRATEGY
# ==========================================
STRATEGY_FILE = strategy_files[0]

# Example:
# STRATEGY_FILE = (
#     "data/compiled_strategies_v2/"
#     "9_20EMA STRATEGY.json"
# )

print(
    f"\nUsing strategy: "
    f"{Path(STRATEGY_FILE).name}"
)

# ==========================================
# LOAD JSON
# ==========================================
with open(
    STRATEGY_FILE,
    "r",
    encoding="utf-8"
) as f:

    strategy = json.load(f)

# ==========================================
# DOWNLOAD DATA
# ==========================================
logger.info(
    "Downloading market data..."
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

# ==========================================
# COMPUTE FEATURES
# ==========================================
logger.info(
    "Computing features..."
)

data = compute_features(
    data
)

# ==========================================
# GENERATE SIGNALS
# ==========================================
logger.info(
    "Generating DSL signals..."
)

entries = generate_dsl_signals(

    strategy[
        "compiled_entry_logic"
    ],

    data
)

# ==========================================
# VALIDATE SIGNALS
# ==========================================
if entries is None:

    raise ValueError(
        "No signals generated."
    )

signal_count = int(
    entries.sum()
)

print(
    f"\nSignals Found: "
    f"{signal_count}"
)

if signal_count == 0:

    raise ValueError(
        "Signal count is zero."
    )

# ==========================================
# SIMPLE EXIT LOGIC
# ==========================================
exits = ~entries

# ==========================================
# BACKTEST
# ==========================================
logger.info(
    "Running backtest..."
)

portfolio = run_backtest(
    data["Close"],
    entries,
    exits
)

# ==========================================
# METRICS
# ==========================================
metrics = calculate_metrics(
    portfolio
)

print(
    "\n===== RESULTS ====="
)

for key, value in metrics.items():

    print(
        f"{key}: {value}"
    )

# ==========================================
# REPORT
# ==========================================
report_path = save_report(
    portfolio,
    strategy["name"]
)

print(
    f"\nReport saved to:\n"
    f"{report_path}"
)