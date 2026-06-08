from pathlib import Path

import json
import yfinance as yf

from loguru import logger

from strategy_adapter import (
    adapt_strategy
)

from portfolio_engine import (
    run_backtest
)

from metrics_engine import (
    calculate_metrics
)

from report_generator import (
    save_report
)

# ==========================================
# LOAD STRATEGY
# ==========================================
strategy_files = list(
    Path(
        "data/compiled_strategies"
    ).glob("*.json")
)

if len(strategy_files) == 0:

    raise ValueError(
        "No compiled strategies found."
    )

STRATEGY_FILE = strategy_files[35]
STRATEGY_FILE = "/Users/pavan/Downloads/alphaforge/data/compiled_strategies/GAUTAM JHA TRADING STRATEGY.json"
print("Strategy file: ", STRATEGY_FILE)
# ==========================================
# LOAD STRATEGY JSON
# ==========================================
with open(
    STRATEGY_FILE,
    "r",
    encoding="utf-8"
) as f:

    strategy_data = json.load(f)

# ==========================================
# DOWNLOAD MARKET DATA
# ==========================================
logger.info(
    "Downloading market data..."
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

# ==========================================
# FIX DATAFRAME SHAPE
# ==========================================
data.columns = data.columns.get_level_values(0)

close = data["Close"].squeeze()

# ==========================================
# ADAPT STRATEGY
# ==========================================
adapted = adapt_strategy(
    strategy_data,
    data
)

signals = adapted["signals"]

# ==========================================
# HANDLE SIGNALS
# ==========================================
from concept_analyzer import (
    analyze_unknown_conditions
)

if len(signals) == 0:

    unknown_conditions = (
        analyze_unknown_conditions(
            strategy_data
        )
    )

    print(
        "\n=== UNKNOWN CONDITIONS ==="
    )

    for condition in unknown_conditions:

        print(f"- {condition}")

    raise ValueError(
        "No valid signals generated."
    )

# ==========================================
# USE FIRST SIGNAL
# ==========================================
entries = signals[0]

# SIMPLE EXIT LOGIC
exits = ~entries

# ==========================================
# RUN BACKTEST
# ==========================================
portfolio = run_backtest(
    close,
    entries,
    exits
)

# ==========================================
# CALCULATE METRICS
# ==========================================
metrics = calculate_metrics(
    portfolio
)

# ==========================================
# PRINT METRICS
# ==========================================
print("\n===== BACKTEST RESULTS =====")

for key, value in metrics.items():

    print(f"{key}: {value}")

# ==========================================
# SAVE REPORT
# ==========================================
report_path = save_report(
    portfolio,
    strategy_data["name"]
)

print(
    f"\nReport saved to: "
    f"{report_path}"
)
from experiments.experiment_tracker import (
    track_experiment
)

experiment = track_experiment(
    strategy_name=
    strategy_data["name"],

    metrics=metrics,

    ontology_version="v1"
)

print(
    "\nExperiment tracked:"
)

print(experiment)

from experiments.insight_engine import (
    generate_insight
)

insight = generate_insight(
    strategy_data["name"],
    metrics
)

print(
    "\n===== AI INSIGHTS ====="
)

print(insight)

from experiments.regime_detector import (
    detect_regime
)

regimes = detect_regime(
    data
)

print(
    "\n===== MARKET REGIMES ====="
)

print(
    regimes.value_counts()
)