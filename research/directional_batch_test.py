from pathlib import Path
import json
import pandas as pd
import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

from backtesting.dsl_signal_engine_v2 import (
    generate_directional_signals
)

# ==========================================
# TEST STRATEGIES
# ==========================================

STRATEGIES = [

    "EMA Crossover Trading Strategy (1).json",

    "9&20EMA STRATEGY.json",

    "3 MOVING AVERAGE TRADING SETUP.json"
]

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

results = []

# ==========================================
# LOOP
# ==========================================

for filename in STRATEGIES:

    try:

        path = Path(
            "data/compiled_strategies_v3"
        ) / filename

        strategy = json.loads(
            path.read_text()
        )

        compiled_logic = strategy.get(
            "compiled_entry_logic",
            []
        )

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

        portfolio = vbt.Portfolio.from_signals(
            close=data["Close"].astype(float),
            entries=long_entries,
            exits=long_exits,
            init_cash=100000,
            freq="1D"
        )

        results.append({

            "strategy":
            strategy["name"],

            "signals":
            int(
                long_entries.sum()
            ),

            "trades":
            int(
                portfolio.trades.count()
            ),

            "return":
            round(
                float(
                    portfolio.total_return()
                ),
                4
            ),

            "sharpe":
            round(
                float(
                    portfolio.sharpe_ratio()
                ),
                4
            ),

            "win_rate":
            round(
                float(
                    portfolio.trades.win_rate()
                ),
                4
            ),

            "max_dd":
            round(
                float(
                    portfolio.max_drawdown()
                ),
                4
            )
        })

    except Exception as e:

        print(
            f"{filename}: {e}"
        )

# ==========================================
# RESULTS
# ==========================================

df = pd.DataFrame(
    results
)

print()
print("=" * 70)
print("DIRECTIONAL ENGINE V2")
print("=" * 70)

print(df)