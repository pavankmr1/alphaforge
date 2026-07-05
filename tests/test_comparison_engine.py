from experiments.comparison_engine import compare_runs, rank_runs
from experiments.runner import save_json


def write_run(path, run_id, total_pnl, win_rate=0.5):
    path.mkdir()

    report = {
        "run_id": run_id,
        "strategy": "unicorn",
        "symbol": "nifty",
        "period": {
            "start": "2025-01-01",
            "end": "2025-01-31",
        },
        "metrics": {
            "total_pnl": total_pnl,
            "win_rate": win_rate,
            "total_trades": 10,
        },
    }

    save_json(path / "report.json", report)
    save_json(path / "metrics.json", report["metrics"])
    save_json(
        path / "config.json",
        {
            "strategy": "unicorn",
            "symbol": "nifty",
        },
    )


def test_rank_runs_orders_by_metric(tmp_path):
    write_run(tmp_path / "2026-07-05_001", "2026-07-05_001", -10)
    write_run(tmp_path / "2026-07-05_002", "2026-07-05_002", 25)

    df = rank_runs(tmp_path, sort_by="total_pnl")

    assert df.iloc[0]["run_id"] == "2026-07-05_002"
    assert df.iloc[0]["total_pnl"] == 25


def test_compare_runs_calculates_numeric_deltas(tmp_path):
    first = tmp_path / "2026-07-05_001"
    second = tmp_path / "2026-07-05_002"

    write_run(first, "2026-07-05_001", -10, win_rate=0.4)
    write_run(second, "2026-07-05_002", 25, win_rate=0.6)

    df = compare_runs(first, second)
    total_pnl = df[df["metric"] == "total_pnl"].iloc[0]

    assert total_pnl["delta"] == 35
