
from pathlib import Path
import json
import pandas as pd
import yfinance as yf

from loguru import logger

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
# CONFIG
# ==========================================
STRATEGY_DIR = Path(
    "data/compiled_strategies_v3"
)

OUTPUT_FILE = Path(
    "data/batch_results/leaderboard_2.csv"
)

MIN_SIGNALS = 5

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

logger.info(
    "Computing features..."
)

data = compute_features(
    data
)

# ==========================================
# RESULTS
# ==========================================
results = []

success_count = 0
failed_count = 0
skipped_count = 0

files = list(
    STRATEGY_DIR.glob("*.json")
)
# TARGET_STRATEGIES = [

#     "9&20EMA STRATEGY.json",

#     "ANISH SINGH VWAP STRATEGY.json",

#     "3 MOVING AVERAGE TRADING SETUP.json",

#     "VWAP STRATEGY OF DEVANSHRAIYT .json",

#     "EMA Crossover Trading Strategy (1).json",

#     "EMA REJECTION STRATEGY.json"
# ]

# files = [

#     STRATEGY_DIR / name

#     for name in TARGET_STRATEGIES
# ]
logger.info(
    f"Found {len(files)} strategies"
)

# ==========================================
# LOOP STRATEGIES
# ==========================================
for file in files:
    if "EMA" not in file.name.upper():
        continue

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

        # ==================================
        # GENERATE SIGNALS
        # ==================================
        long_entries, long_exits = (
            generate_directional_signals(
                compiled_logic,
                data
            )
        )
        if long_entries is None:
            continue
        long_exits = (
            long_exits
            .shift(1)
            .fillna(False)
            .astype(bool)
        )

        if long_entries is None:

            print(
                f"SKIPPED -> {file.name} (long_entries=None)"
            )

            skipped_count += 1
            continue

        signal_count = int(
            long_entries.sum()
        )

        print(
            f"SIGNALS -> {file.name}: {signal_count}"
        )

        if signal_count < MIN_SIGNALS:

            print(
                f"SKIPPED -> {file.name} "
                f"(signals={signal_count})"
            )

            skipped_count += 1
            continue

        # ==================================
        # CLEAN SIGNALS
        # ==================================
        long_entries = (
            long_entries
            .fillna(False)
            .astype(bool)
        )

        # ==================================
        # TEMP EXIT RULE
        # ==================================
        from backtesting.exit_engine import (
            generate_exits
        )

        long_exits = generate_exits(
            long_entries,
            data,
            strategy
        )

        print(
            f"long_entries dtype: {long_entries.dtype}"
        )

        print(
            f"long_exits dtype: {long_exits.dtype}"
        )

        assert long_entries.dtype == bool
        assert long_exits.dtype == bool

        print(
            f"BACKTESTING -> {file.name}"
        )
        print(long_entries.dtype)
        print(long_exits.dtype)

        portfolio = run_backtest(
            close=data["Close"],
            entries=long_entries,
            exits=long_exits
        )

        print(
            f"PORTFOLIO OK -> {file.name}"
        )

        total_return = float(
            portfolio.total_return()
        )

        sharpe_ratio = float(
            portfolio.sharpe_ratio()
        )

        win_rate = float(
            portfolio.trades.win_rate()
        )

        max_drawdown = float(
            portfolio.max_drawdown()
        )

        print(
            f"STATS OK -> {file.name}"
        )

        if pd.isna(sharpe_ratio):
            sharpe_ratio = 0.0

        if pd.isna(win_rate):
            win_rate = 0.0

        if pd.isna(max_drawdown):
            max_drawdown = 0.0

        results.append({

            "strategy":
            strategy.get(
                "name",
                file.stem
            ),

            "signals":
            signal_count,

            "trades":
            int(
                portfolio.trades.count()
            ),

            "total_return":
            round(
                total_return,
                4
            ),

            "sharpe_ratio":
            round(
                sharpe_ratio,
                4
            ),

            "win_rate":
            round(
                win_rate,
                4
            ),

            "max_drawdown":
            round(
                max_drawdown,
                4
            ),

            "signal_trade_ratio":
            round(
                signal_count /
                max(
                    int(portfolio.trades.count()),
                    1
                ),
                2
            ),

            "avg_return_per_trade":
            round(
                total_return /
                max(
                    int(portfolio.trades.count()),
                    1
                ),
                4
            ),
        })

        print(
            f"RESULT SAVED -> {file.name}"
        )

        success_count += 1

    except Exception as e:

        failed_count += 1

        print(
            f"FAILED -> {file.name}"
        )

        print(type(e).__name__)
        print(str(e))

        logger.exception(e)
# ==========================================
# SUMMARY
# ==========================================
print()

print("=" * 50)
print("ALPHAFORGE BATCH BACKTEST")
print("=" * 50)

print(
    f"Strategies Found: {len(files)}"
)

print(
    f"Successful: {success_count}"
)

print(
    f"Skipped: {skipped_count}"
)

print(
    f"Failed: {failed_count}"
)

# ==========================================
# SAVE RESULTS
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
        [
            "sharpe_ratio",
            "win_rate",
            "total_return"
        ],
        ascending=False
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True   
    )

    df = df[
        df["signal_trade_ratio"] < 20
    ]
    df = df[
        df["trades"] >= 5
    ]
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    TOP_FILE = Path(
        "data/batch_results/top_strategies.csv"
    )

    df.head(10).to_csv(
        TOP_FILE,
        index=False
    )
    print(
        "\nTOP 20 STRATEGIES\n"
    )

    print(
        df[
            [
                "strategy",
                "signals",
                "trades",
                "total_return",
                "sharpe_ratio",
                "win_rate",
                "max_drawdown"
            ]
        ]
        .head(20)
    )

    print(
        f"\nSaved: {OUTPUT_FILE}"
    )