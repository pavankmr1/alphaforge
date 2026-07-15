# AlphaForge Status

## Completed
- Corpus compilation
- Validator
- Feature engine
- Backtesting
- Leaderboard
- Diagnostics
- Rule mapping inventory
- Invalid rule analysis
- AlphaForge V1 engine milestone

## Current Sprint
- AlphaForge V2 Experiment System

## Experiment Runner
```bash
python research/run_experiment.py \
    --strategy unicorn \
    --symbol nifty \
    --start 2025-01-01 \
    --end 2025-12-31
```

Each run writes immutable artifacts to `experiments/runs/<date>_<number>/`:
- `config.json`
- `trades.csv`
- `equity.csv`
- `metrics.json`
- `report.json`
- `event_log.json`

Rank saved experiments:
```bash
python research/compare_experiments.py \
    --sort-by total_pnl
```

Run walk-forward windows:
```bash
python research/run_walk_forward.py \
    --strategy unicorn \
    --symbol nifty \
    --start 2021-01-01 \
    --end 2025-12-31 \
    --train-months 12 \
    --test-months 3
```

Run Monte Carlo on a saved experiment:
```bash
python research/run_monte_carlo.py \
    experiments/runs/2026-07-05_001 \
    --simulations 1000
```

## Next
- Exit Engine V2
- Hyperparameter Sweeps
- Multi Asset Testing



# AlphaForge Status

## V1 — Trading Engine ✅

- Replay Engine
- Trade Manager
- Portfolio Engine
- Strategy Registry
- Unicorn Strategy

Status: COMPLETE

---

## V2 — Research Infrastructure ✅

- Experiment Runner
- Experiment Comparison
- Walk Forward
- Monte Carlo
- Experiment Index

Status: COMPLETE

---

## V3 — Research Intelligence ✅

- Research Score
- Parameter Sweep
- Grid Search
- Research Analyzer
- Strategy Report
- Research Dashboard CLI

Status: COMPLETE

---

## Next Milestone

V4 — Paper Trading