from pathlib import Path
import json

import yfinance as yf

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
# REPORT
# ==========================================

print()
print("=" * 60)
print(strategy["name"])
print("=" * 60)

for item in compiled_logic:

    print()
    print(
        "CONDITION:"
    )

    print(
        item.get(
            "original_condition"
        )
    )

    dsl = item.get(
        "dsl"
    )

    if not dsl:

        print(
            "No DSL"
        )
        continue

    rules = dsl.get(
        "rules",
        []
    )

    for rule in rules:

        signal = execute_rule(
            rule,
            data
        )

        if signal is None:

            print(
                "FAILED:",
                rule
            )

            continue

        print()

        print(
            "RULE:",
            rule
        )

        print(
            "SIGNALS:",
            int(
                signal.sum()
            )
        )