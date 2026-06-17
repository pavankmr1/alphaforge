from pathlib import Path
import pandas as pd

LEADERBOARD = Path(
    "data/batch_results/leaderboard.csv"
)

df = pd.read_csv(
    LEADERBOARD
)

print()
print("=" * 60)
print("TOP STRATEGY DIAGNOSTICS")
print("=" * 60)

for _, row in df.head(10).iterrows():

    print()
    print("-" * 60)

    print(
        f"Strategy: {row['strategy']}"
    )

    print(
        f"Signals: {row['signals']}"
    )

    print(
        f"Trades: {row['trades']}"
    )

    print(
        f"Signal/Trade Ratio: "
        f"{row['signal_trade_ratio']}"
    )

    print(
        f"Sharpe: "
        f"{row['sharpe_ratio']}"
    )

    print(
        f"Win Rate: "
        f"{row['win_rate']}"
    )

    print(
        f"Return: "
        f"{row['total_return']}"
    )