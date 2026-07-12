import argparse

from experiments.parameter_sweep import ParameterSweep
from backtesting.strategies.unicorn import UnicornStrategy


parser = argparse.ArgumentParser()

parser.add_argument("--strategy", default="UNICORN")
parser.add_argument("--symbol", default="nifty")
parser.add_argument("--parameter", default="min_gap_atr")
parser.add_argument("--start")
parser.add_argument("--end")

args = parser.parse_args()

space = UnicornStrategy.parameter_space()

if args.parameter not in space:

    raise ValueError(
        f"Unknown parameter: {args.parameter}"
    )

runner = ParameterSweep()

results = runner.run(

    strategy=args.strategy,

    symbol=args.symbol,

    parameter=args.parameter,

    values=space[args.parameter],

    start=args.start,

    end=args.end,

)

# results = results.sort_values(

#     "profit_factor",

#     ascending=False

# )
results = results.sort_values(
    "research_score",
    ascending=False
)
print()

print("=" * 80)
print("PARAMETER SWEEP")
print("=" * 80)

# print(results)
best = results.iloc[0]

print()

print("=" * 80)

print("BEST CONFIGURATION")

print("=" * 80)

print()

print(best)

print()

print("=" * 80)

print("LEADERBOARD")

print("=" * 80)

print()

print(results)

results.to_csv(

    "parameter_sweep_results.csv",

    index=False

)

print()

print("Saved parameter_sweep_results.csv")