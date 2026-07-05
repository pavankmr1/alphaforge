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

## Next
- Exit Engine V2
- Walk Forward Testing
- Multi Asset Testing
