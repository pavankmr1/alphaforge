from experiments.experiment_index import ExperimentIndex

index = ExperimentIndex()

print()

print("=" * 80)
print("ALPHAFORGE LEADERBOARD")
print("=" * 80)

print()

print(index.top(n=20))