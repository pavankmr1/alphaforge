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
# CONDITION LOGIC TEST
# ==========================================

final_signal = None

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

    condition_signal = None

    for rule in rules:

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

        if condition_signal is None:

            condition_signal = signal

        else:

            # OR INSIDE CONDITION
            condition_signal = (
                condition_signal
                |
                signal
            )

    if condition_signal is None:
        continue

    print(
        "CONDITION TOTAL:",
        int(
            condition_signal.sum()
        )
    )

    if final_signal is None:

        final_signal = condition_signal

    else:

        # AND BETWEEN CONDITIONS
        final_signal = (
            final_signal
            &
            condition_signal
        )

# ==========================================
# FINAL RESULT
# ==========================================

print()
print("=" * 60)
print("FINAL CONDITION LOGIC RESULT")
print("=" * 60)

if final_signal is not None:

    print(
        "FINAL SIGNALS:",
        int(
            final_signal.sum()
        )
    )

    print()

    print(
        final_signal[
            final_signal
        ].index
    )

else:

    print(
        "No signals generated."
    )