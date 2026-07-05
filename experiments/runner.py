import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from itertools import count
from pathlib import Path

import pandas as pd

from backtesting.feature_engine import compute_features
from backtesting.portfolio_engine import PortfolioEngine
from backtesting.replay_engine import ReplayEngine
from backtesting.strategy_registry import StrategyRegistry
from backtesting.strategies import unicorn  # noqa: F401


DEFAULT_DATA_PATHS = {
    "nifty": {
        "1m": Path("data/raw/nifty_1m_master.csv"),
        "5m": Path("data/processed/nifty_5m_master.csv"),
    }
}

RUNS_DIR = Path("experiments/runs")


def run_experiment(
    strategy_name,
    symbol,
    start=None,
    end=None,
    output_root=RUNS_DIR,
    data_paths=None,
    parameters=None,
):
    config = build_config(
        strategy_name=strategy_name,
        symbol=symbol,
        start=start,
        end=end,
        data_paths=data_paths,
        parameters=parameters,
    )

    run_dir = create_run_dir(output_root)

    save_json(run_dir / "config.json", config)

    df_1m, df_5m = load_market_data(
        symbol=symbol,
        start=start,
        end=end,
        data_paths=data_paths,
    )

    df_1m = compute_features(df_1m)
    df_5m = compute_features(df_5m)

    strategy = StrategyRegistry.create(strategy_name)
    replay = ReplayEngine(strategy)
    replay.run(df_5m, df_1m)

    trades = replay.trade_manager.closed_trades
    portfolio = PortfolioEngine(trades)

    metrics = build_metrics(portfolio)
    report = build_report(
        config=config,
        metrics=metrics,
        run_dir=run_dir,
        started_at=config["created_at"],
    )

    trades_df = trades_to_dataframe(trades)
    equity_df = equity_curve_from_trades(trades)
    event_log = serialize_value(strategy.context.event_log)

    trades_df.to_csv(run_dir / "trades.csv", index=False)
    equity_df.to_csv(run_dir / "equity.csv", index=False)
    save_json(run_dir / "metrics.json", metrics)
    save_json(run_dir / "report.json", report)
    save_json(run_dir / "event_log.json", event_log)

    return {
        "run_dir": str(run_dir),
        "config": config,
        "metrics": metrics,
        "trades": len(trades),
    }


def build_config(
    strategy_name,
    symbol,
    start=None,
    end=None,
    data_paths=None,
    parameters=None,
):
    resolved_paths = resolve_data_paths(symbol, data_paths)

    return {
        "created_at": utc_now(),
        "strategy": strategy_name.lower(),
        "symbol": symbol.lower(),
        "start": start,
        "end": end,
        "timeframes": ["5m", "1m"],
        "data_paths": {
            timeframe: str(path)
            for timeframe, path in resolved_paths.items()
        },
        "parameters": parameters or {},
    }


def load_market_data(symbol, start=None, end=None, data_paths=None):
    paths = resolve_data_paths(symbol, data_paths)

    df_1m = load_ohlcv_csv(paths["1m"])
    df_5m = load_ohlcv_csv(paths["5m"])

    return (
        filter_dates(df_1m, start, end),
        filter_dates(df_5m, start, end),
    )


def load_ohlcv_csv(path):
    df = pd.read_csv(path)

    if "datetime" not in df.columns:
        raise ValueError(f"Missing datetime column in {path}")

    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()

    rename = {
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }

    df = df.rename(columns=rename)

    required = ["Open", "High", "Low", "Close", "Volume"]
    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing OHLCV columns in {path}: {missing}")

    return df[required]


def filter_dates(df, start=None, end=None):
    if start:
        df = df.loc[df.index >= pd.Timestamp(start)]

    if end:
        df = df.loc[df.index <= pd.Timestamp(end)]

    return df


def resolve_data_paths(symbol, data_paths=None):
    if data_paths is not None:
        return {
            "1m": Path(data_paths["1m"]),
            "5m": Path(data_paths["5m"]),
        }

    symbol_key = symbol.lower()

    if symbol_key not in DEFAULT_DATA_PATHS:
        raise ValueError(
            f"No default data paths configured for symbol: {symbol}"
        )

    return DEFAULT_DATA_PATHS[symbol_key]


def create_run_dir(output_root=RUNS_DIR, now=None):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    date_prefix = (now or datetime.now()).strftime("%Y-%m-%d")

    for run_number in count(1):
        run_dir = output_root / f"{date_prefix}_{run_number:03d}"

        try:
            run_dir.mkdir()
            return run_dir
        except FileExistsError:
            continue


def build_metrics(portfolio):
    return {
        "total_trades": portfolio.total_trades(),
        "wins": len(portfolio.winners()),
        "losses": len(portfolio.losers()),
        "win_rate": safe_float(portfolio.win_rate()),
        "profit_factor": safe_float(portfolio.profit_factor()),
        "average_rr": safe_float(portfolio.average_rr()),
        "total_pnl": safe_float(portfolio.total_pnl()),
        "average_winner": safe_float(portfolio.average_winner()),
        "average_loser": safe_float(portfolio.average_loser()),
        "best_trade_pnl": trade_pnl(portfolio.best_trade()),
        "worst_trade_pnl": trade_pnl(portfolio.worst_trade()),
    }


def build_report(config, metrics, run_dir, started_at):
    return {
        "run_id": Path(run_dir).name,
        "started_at": started_at,
        "completed_at": utc_now(),
        "strategy": config["strategy"],
        "symbol": config["symbol"],
        "period": {
            "start": config["start"],
            "end": config["end"],
        },
        "metrics": metrics,
        "artifacts": {
            "config": "config.json",
            "trades": "trades.csv",
            "equity": "equity.csv",
            "metrics": "metrics.json",
            "event_log": "event_log.json",
        },
    }


def trades_to_dataframe(trades):
    rows = []

    for trade in trades:
        signal = trade.signal

        rows.append({
            "strategy": signal.strategy,
            "direction": signal.direction,
            "timeframe": signal.timeframe,
            "entry_time": signal.entry_time,
            "entry_price": signal.entry_price,
            "stop_loss": signal.stop_loss,
            "target": signal.target,
            "exit_time": trade.exit_time,
            "exit_price": trade.exit_price,
            "pnl": trade.pnl,
            "rr": trade.rr,
            "reason": trade.reason,
            "confidence": signal.confidence,
        })

    return pd.DataFrame(rows)


def equity_curve_from_trades(trades):
    rows = []
    equity = 0.0

    for trade in trades:
        equity += trade.pnl

        rows.append({
            "datetime": trade.exit_time,
            "equity": equity,
            "pnl": trade.pnl,
        })

    return pd.DataFrame(rows)


def save_json(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            serialize_value(payload),
            f,
            indent=4,
            allow_nan=False,
        )


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def serialize_value(value):
    if is_dataclass(value):
        return serialize_value(asdict(value))

    if isinstance(value, dict):
        return {
            str(key): serialize_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            serialize_value(item)
            for item in value
        ]

    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()

    return value


def safe_float(value):
    if value == float("inf"):
        return None

    return float(value)


def trade_pnl(trade):
    if trade is None:
        return 0.0

    return safe_float(trade.pnl)


def utc_now():
    return datetime.now(timezone.utc).isoformat()
