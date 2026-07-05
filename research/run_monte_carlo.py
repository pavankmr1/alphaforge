import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.monte_carlo import run_monte_carlo  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run Monte Carlo analysis for a saved AlphaForge experiment."
    )

    parser.add_argument("run_dir")
    parser.add_argument("--simulations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--ruin-threshold", type=float, default=0.0)

    return parser.parse_args()


def main():
    args = parse_args()

    result = run_monte_carlo(
        run_dir=args.run_dir,
        simulations=args.simulations,
        seed=args.seed,
        ruin_threshold=args.ruin_threshold,
    )

    print()
    print("=" * 80)
    print("MONTE CARLO COMPLETE")
    print("=" * 80)
    print("Output directory:", result["output_dir"])
    print("Summary:")

    for key, value in result["summary"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
