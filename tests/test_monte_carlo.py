import pandas as pd

from experiments.monte_carlo import (
    max_drawdown,
    run_monte_carlo,
    simulate_equity_paths,
)
from experiments.runner import save_json


def test_simulate_equity_paths_is_deterministic_with_seed():
    pnl = [10, -5, 20]

    first = simulate_equity_paths(pnl, simulations=3, seed=7)
    second = simulate_equity_paths(pnl, simulations=3, seed=7)

    assert first.equals(second)
    assert first.shape == (3, 3)


def test_max_drawdown_uses_peak_to_trough_distance():
    assert max_drawdown([10, 15, 7, 20, 18]) == 8.0


def test_run_monte_carlo_writes_artifacts(tmp_path):
    run_dir = tmp_path / "2026-07-05_001"
    run_dir.mkdir()

    pd.DataFrame({
        "pnl": [10, -5, 20, -3],
    }).to_csv(run_dir / "trades.csv", index=False)

    save_json(
        run_dir / "report.json",
        {
            "run_id": run_dir.name,
            "strategy": "unicorn",
            "symbol": "nifty",
            "period": {
                "start": "2025-01-01",
                "end": "2025-01-31",
            },
        },
    )

    result = run_monte_carlo(
        run_dir,
        simulations=10,
        seed=1,
    )

    output_dir = run_dir / "monte_carlo"

    assert result["summary"]["trade_count"] == 4
    assert (output_dir / "monte_carlo_summary.json").exists()
    assert (output_dir / "monte_carlo_paths.csv").exists()
    assert (output_dir / "monte_carlo_percentiles.csv").exists()


def test_run_monte_carlo_handles_empty_trade_file(tmp_path):
    run_dir = tmp_path / "2026-07-05_001"
    run_dir.mkdir()

    (run_dir / "trades.csv").write_text("")

    result = run_monte_carlo(run_dir, simulations=10)

    assert result["summary"]["trade_count"] == 0
    assert result["summary"]["probability_profitable"] == 0.0
