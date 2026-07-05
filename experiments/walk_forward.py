from datetime import datetime
from pathlib import Path

import pandas as pd

from experiments.runner import RUNS_DIR, run_experiment, save_json


def build_walk_forward_windows(
    start,
    end,
    train_months=12,
    test_months=3,
):
    start_ts = pd.Timestamp(start)
    end_ts = pd.Timestamp(end)

    if train_months <= 0:
        raise ValueError("train_months must be positive.")

    if test_months <= 0:
        raise ValueError("test_months must be positive.")

    windows = []
    train_start = start_ts

    while True:
        train_end = train_start + pd.DateOffset(months=train_months)
        test_start = train_end
        test_end = test_start + pd.DateOffset(months=test_months)

        if test_start > end_ts:
            break

        if test_end > end_ts:
            test_end = end_ts

        windows.append({
            "train_start": format_date(train_start),
            "train_end": format_date(train_end),
            "test_start": format_date(test_start),
            "test_end": format_date(test_end),
        })

        if test_end >= end_ts:
            break

        train_start = train_start + pd.DateOffset(months=test_months)

    return windows


def run_walk_forward(
    strategy_name,
    symbol,
    start,
    end,
    train_months=12,
    test_months=3,
    output_root=RUNS_DIR,
    data_paths=None,
):
    campaign_dir = create_walk_forward_dir(output_root)
    windows = build_walk_forward_windows(
        start=start,
        end=end,
        train_months=train_months,
        test_months=test_months,
    )

    results = []

    for index, window in enumerate(windows, start=1):
        run_result = run_experiment(
            strategy_name=strategy_name,
            symbol=symbol,
            start=window["test_start"],
            end=window["test_end"],
            output_root=campaign_dir,
            data_paths=data_paths,
            parameters={
                "walk_forward_window": index,
                "train_start": window["train_start"],
                "train_end": window["train_end"],
            },
        )

        results.append({
            "window": index,
            "train_start": window["train_start"],
            "train_end": window["train_end"],
            "test_start": window["test_start"],
            "test_end": window["test_end"],
            "run_dir": run_result["run_dir"],
            **run_result["metrics"],
        })

    summary = pd.DataFrame(results)
    summary.to_csv(campaign_dir / "walk_forward_summary.csv", index=False)

    payload = {
        "strategy": strategy_name.lower(),
        "symbol": symbol.lower(),
        "start": start,
        "end": end,
        "train_months": train_months,
        "test_months": test_months,
        "windows": results,
    }

    save_json(campaign_dir / "walk_forward_summary.json", payload)

    return {
        "campaign_dir": str(campaign_dir),
        "windows": len(windows),
        "summary": results,
    }


def create_walk_forward_dir(output_root=RUNS_DIR, now=None):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    timestamp = (now or datetime.now()).strftime("%Y-%m-%d_%H%M%S")
    campaign_dir = output_root / f"walk_forward_{timestamp}"

    if not campaign_dir.exists():
        campaign_dir.mkdir()
        return campaign_dir

    suffix = 2

    while True:
        candidate = output_root / f"walk_forward_{timestamp}_{suffix}"

        if not candidate.exists():
            candidate.mkdir()
            return candidate

        suffix += 1


def format_date(value):
    return pd.Timestamp(value).date().isoformat()
