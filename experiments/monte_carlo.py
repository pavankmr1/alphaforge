from pathlib import Path

import numpy as np
import pandas as pd
from pandas.errors import EmptyDataError

from experiments.runner import load_json, save_json


def run_monte_carlo(
    run_dir,
    simulations=1000,
    seed=42,
    ruin_threshold=0.0,
):
    run_dir = Path(run_dir)
    trades_path = run_dir / "trades.csv"

    if not trades_path.exists():
        raise ValueError(f"Missing trades file: {trades_path}")

    try:
        trades = pd.read_csv(trades_path)
    except EmptyDataError:
        trades = pd.DataFrame(columns=["pnl"])

    if "pnl" not in trades.columns:
        raise ValueError(f"Missing pnl column in {trades_path}")

    pnl = trades["pnl"].dropna().to_numpy(dtype=float)

    if len(pnl) == 0:
        paths = pd.DataFrame()
        percentiles = pd.DataFrame()
        summary = build_empty_summary(
            run_dir=run_dir,
            simulations=simulations,
            seed=seed,
            ruin_threshold=ruin_threshold,
        )
    else:
        paths = simulate_equity_paths(
            pnl=pnl,
            simulations=simulations,
            seed=seed,
        )
        percentiles = calculate_path_percentiles(paths)
        summary = calculate_summary(
            run_dir=run_dir,
            pnl=pnl,
            paths=paths,
            simulations=simulations,
            seed=seed,
            ruin_threshold=ruin_threshold,
        )

    output_dir = run_dir / "monte_carlo"
    output_dir.mkdir(exist_ok=True)

    paths.to_csv(output_dir / "monte_carlo_paths.csv", index=False)
    percentiles.to_csv(output_dir / "monte_carlo_percentiles.csv", index=False)
    save_json(output_dir / "monte_carlo_summary.json", summary)

    return {
        "output_dir": str(output_dir),
        "summary": summary,
    }


def simulate_equity_paths(pnl, simulations=1000, seed=42):
    if simulations <= 0:
        raise ValueError("simulations must be positive.")

    rng = np.random.default_rng(seed)
    pnl = np.asarray(pnl, dtype=float)

    samples = rng.choice(
        pnl,
        size=(simulations, len(pnl)),
        replace=True,
    )

    equity = samples.cumsum(axis=1)

    columns = [
        f"trade_{index}"
        for index in range(1, len(pnl) + 1)
    ]

    return pd.DataFrame(equity, columns=columns)


def calculate_path_percentiles(paths):
    rows = []

    for trade_number, column in enumerate(paths.columns, start=1):
        values = paths[column]

        rows.append({
            "trade": trade_number,
            "p05": float(values.quantile(0.05)),
            "p25": float(values.quantile(0.25)),
            "p50": float(values.quantile(0.50)),
            "p75": float(values.quantile(0.75)),
            "p95": float(values.quantile(0.95)),
        })

    return pd.DataFrame(rows)


def calculate_summary(
    run_dir,
    pnl,
    paths,
    simulations,
    seed,
    ruin_threshold,
):
    final_pnl = paths.iloc[:, -1]
    max_drawdowns = paths.apply(max_drawdown, axis=1)
    min_equity = paths.min(axis=1)

    base = {
        "source_run": Path(run_dir).name,
        "simulations": simulations,
        "seed": seed,
        "trade_count": len(pnl),
        "ruin_threshold": ruin_threshold,
        "original_total_pnl": float(np.sum(pnl)),
        "original_average_trade": float(np.mean(pnl)),
    }

    report = run_report(run_dir)

    if report:
        base["strategy"] = report.get("strategy")
        base["symbol"] = report.get("symbol")
        base["period"] = report.get("period")

    base.update({
        "probability_profitable": float((final_pnl > 0).mean()),
        "risk_of_ruin": float((min_equity <= ruin_threshold).mean()),
        "median_final_pnl": float(final_pnl.quantile(0.50)),
        "p05_final_pnl": float(final_pnl.quantile(0.05)),
        "p95_final_pnl": float(final_pnl.quantile(0.95)),
        "worst_final_pnl": float(final_pnl.min()),
        "best_final_pnl": float(final_pnl.max()),
        "median_max_drawdown": float(max_drawdowns.quantile(0.50)),
        "p95_max_drawdown": float(max_drawdowns.quantile(0.95)),
        "worst_max_drawdown": float(max_drawdowns.max()),
    })

    return base


def build_empty_summary(
    run_dir,
    simulations,
    seed,
    ruin_threshold,
):
    return {
        "source_run": Path(run_dir).name,
        "simulations": simulations,
        "seed": seed,
        "trade_count": 0,
        "ruin_threshold": ruin_threshold,
        "original_total_pnl": 0.0,
        "original_average_trade": 0.0,
        "probability_profitable": 0.0,
        "risk_of_ruin": 0.0,
        "median_final_pnl": 0.0,
        "p05_final_pnl": 0.0,
        "p95_final_pnl": 0.0,
        "worst_final_pnl": 0.0,
        "best_final_pnl": 0.0,
        "median_max_drawdown": 0.0,
        "p95_max_drawdown": 0.0,
        "worst_max_drawdown": 0.0,
    }


def max_drawdown(equity):
    values = np.asarray(equity, dtype=float)
    peak = np.maximum.accumulate(values)
    drawdown = peak - values

    return float(drawdown.max())


def run_report(run_dir):
    report_path = Path(run_dir) / "report.json"

    if not report_path.exists():
        return {}

    return load_json(report_path)
