import json
import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.dsl_signal_engine import (
    generate_dsl_signals
)

# ==========================================
# LOAD STRATEGY
# ==========================================
from pathlib import Path

strategy_files = list(
    Path(
        "data/compiled_strategies_v2"
    ).glob("*.json")
)

strategy_file = strategy_files[0]

print(
    f"Using strategy: {strategy_file.name}"
)

with open(
    strategy_file,
    "r",
    encoding="utf-8"
) as f:

    strategy = json.load(f)

# ==========================================
# DATA
# ==========================================
data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = data.columns.get_level_values(0)

data = compute_features(
    data
)

# ==========================================
# SIGNALS
# ==========================================
entries = generate_dsl_signals(

    strategy[
        "compiled_entry_logic"
    ],

    data
)

print(
    "Signals Found:",
    entries.sum()
)