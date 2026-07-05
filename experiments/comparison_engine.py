from pathlib import Path

import pandas as pd

from experiments.runner import RUNS_DIR, load_json


DEFAULT_COLUMNS = [
    "run_id",
    "strategy",
    "symbol",
    "start",
    "end",
    "total_trades",
    "win_rate",
    "profit_factor",
    "average_rr",
    "total_pnl",
]


def list_experiment_runs(runs_root=RUNS_DIR):
    runs_root = Path(runs_root)

    if not runs_root.exists():
        return []

    runs = []

    for run_dir in sorted(runs_root.iterdir()):
        if not run_dir.is_dir():
            continue

        report_path = run_dir / "report.json"
        config_path = run_dir / "config.json"
        metrics_path = run_dir / "metrics.json"

        if not report_path.exists():
            continue

        runs.append(
            load_run_summary(
                run_dir=run_dir,
                report_path=report_path,
                config_path=config_path,
                metrics_path=metrics_path,
            )
        )

    return runs


def load_run_summary(
    run_dir,
    report_path=None,
    config_path=None,
    metrics_path=None,
):
    run_dir = Path(run_dir)
    report = load_json(report_path or run_dir / "report.json")

    config = {}
    metrics = report.get("metrics", {})

    if (config_path or run_dir / "config.json").exists():
        config = load_json(config_path or run_dir / "config.json")

    if (metrics_path or run_dir / "metrics.json").exists():
        metrics = load_json(metrics_path or run_dir / "metrics.json")

    period = report.get("period", {})

    return {
        "run_id": report.get("run_id", run_dir.name),
        "run_dir": str(run_dir),
        "strategy": report.get("strategy") or config.get("strategy"),
        "symbol": report.get("symbol") or config.get("symbol"),
        "start": period.get("start") or config.get("start"),
        "end": period.get("end") or config.get("end"),
        "started_at": report.get("started_at"),
        "completed_at": report.get("completed_at"),
        **metrics,
    }


def runs_to_dataframe(runs):
    return pd.DataFrame(runs)


def rank_runs(
    runs_root=RUNS_DIR,
    sort_by="total_pnl",
    ascending=False,
):
    df = runs_to_dataframe(
        list_experiment_runs(runs_root)
    )

    if df.empty:
        return df

    if sort_by not in df.columns:
        raise ValueError(
            f"Cannot rank by missing metric: {sort_by}"
        )

    return df.sort_values(
        by=sort_by,
        ascending=ascending,
        na_position="last",
    )


def compare_runs(run_a, run_b):
    left = load_run_summary(run_a)
    right = load_run_summary(run_b)

    metric_names = sorted(
        set(left.keys())
        | set(right.keys())
    )

    rows = []

    for metric in metric_names:
        left_value = left.get(metric)
        right_value = right.get(metric)

        if not is_number(left_value) or not is_number(right_value):
            continue

        rows.append({
            "metric": metric,
            "left": left_value,
            "right": right_value,
            "delta": right_value - left_value,
        })

    return pd.DataFrame(rows)


def select_display_columns(df, columns=None):
    if df.empty:
        return df

    selected = columns or DEFAULT_COLUMNS

    return df[
        [
            column
            for column in selected
            if column in df.columns
        ]
    ]


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)
