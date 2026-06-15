from pathlib import Path
import json
import pandas as pd
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

# ==========================================
# PATHS
# ==========================================
STRATEGY_DIR = Path(
    "data/compiled_strategies_v2"
)

OUTPUT_FILE = Path(
    "data/batch_results/leaderboard.csv"
)

# ==========================================
# MARKET DATA
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

data = compute_features(
    data
)

# ==========================================
# RESULTS
# ==========================================
results = []

files = list(
    STRATEGY_DIR.glob("*.json")
)

logger.info(
    f"Found {len(files)} strategies"
)

for file in files:

    try:

        logger.info(
            f"Testing {file.name}"
        )

        strategy = json.loads(
            file.read_text()
        )

        compiled_logic = strategy.get(
            "compiled_entry_logic",
            []
        )

        entries = generate_dsl_signals(
            compiled_logic,
            data
        )

        if entries is None:
            continue

        if entries.sum() == 0:
            continue

        # ==========================
        # TEMP EXIT LOGIC
        # ==========================
        exits = (
            entries.shift(5)
            .fillna(False)
        )

        portfolio = run_backtest(
            data["Close"],
            entries,
            exits
        )

        results.append({

            "strategy":
            strategy.get(
                "name",
                file.stem
            ),

            "total_return":
            float(
                portfolio.total_return()
            ),

            "sharpe_ratio":
            float(
                portfolio.sharpe_ratio()
            ),

            "win_rate":
            float(
                portfolio.trades.win_rate()
            ),

            "max_drawdown":
            float(
                portfolio.max_drawdown()
            ),

            "signals":
            int(
                entries.sum()
            )
        })

    except Exception as e:

        logger.error(
            f"{file.name}: {e}"
        )

print(
    f"\nStrategies Found: {len(files)}"
)

print(
    f"Strategies Backtested: {len(results)}"
)
# ==========================================
# SAVE
# ==========================================
df = pd.DataFrame(
    results
)

if len(df) == 0:

    print(
        "\nNo valid strategies found."
    )

else:

    df = df.sort_values(
        "sharpe_ratio",
        ascending=False
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nTop Strategies\n")

    print(
        df.head(20)
    )

    print(
        f"\nSaved: {OUTPUT_FILE}"
    )