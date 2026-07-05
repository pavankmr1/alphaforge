import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.runner import run_experiment


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run an AlphaForge experiment."
    )

    parser.add_argument("--strategy", required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--output-root", default="experiments/runs")
    parser.add_argument("--data-1m")
    parser.add_argument("--data-5m")

    return parser.parse_args()


def main():
    args = parse_args()

    data_paths = None

    if args.data_1m or args.data_5m:
        if not args.data_1m or not args.data_5m:
            raise ValueError(
                "Both --data-1m and --data-5m are required when overriding data."
            )

        data_paths = {
            "1m": args.data_1m,
            "5m": args.data_5m,
        }

    result = run_experiment(
        strategy_name=args.strategy,
        symbol=args.symbol,
        start=args.start,
        end=args.end,
        output_root=args.output_root,
        data_paths=data_paths,
    )

    print()
    print("=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)
    print("Run directory:", result["run_dir"])
    print("Trades:", result["trades"])
    print("Metrics:")

    for key, value in result["metrics"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
