import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.comparison_engine import (  # noqa: E402
    compare_runs,
    rank_runs,
    select_display_columns,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="List, rank, or compare AlphaForge experiment runs."
    )

    parser.add_argument("--runs-root", default="experiments/runs")
    parser.add_argument("--sort-by", default="total_pnl")
    parser.add_argument("--ascending", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--csv")
    parser.add_argument("--compare", nargs=2, metavar=("RUN_A", "RUN_B"))

    return parser.parse_args()


def main():
    args = parse_args()

    if args.compare:
        df = compare_runs(args.compare[0], args.compare[1])
    else:
        df = rank_runs(
            runs_root=args.runs_root,
            sort_by=args.sort_by,
            ascending=args.ascending,
        )

        df = select_display_columns(df)

        if args.limit:
            df = df.head(args.limit)

    if args.csv:
        df.to_csv(args.csv, index=False)

    if df.empty:
        print("No experiment runs found.")
        return

    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
