import pandas as pd
import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(
    data
)

entries = (

    (data["EMA21"] > data["EMA9"])

    &

    (
        data["EMA21"].shift(1)
        <=
        data["EMA9"].shift(1)
    )

)

exits = (

    (data["EMA9"] < data["EMA21"])

    &

    (
        data["EMA9"].shift(1)
        >=
        data["EMA21"].shift(1)
    )

)
exits = exits.shift(1).fillna(False)
print()

print(
    data.loc[
        entries,
        ["Close", "EMA9", "EMA21"]
    ]
)

print()

print(
    data.loc[
        exits,
        ["Close", "EMA9", "EMA21"]
    ]
)
print(
    "Entry Signals:",
    int(entries.sum())
)

print(
    "Exit Signals:",
    int(exits.sum())
)

print(
    entries[entries].index
)

print(
    exits[exits].index
)

print(
    "Same Dates:",
    (
        entries[entries].index
        ==
        exits[exits].index
    ).all()
)

entries = (
    entries
    .fillna(False)
    .astype(bool)
)

exits = (
    exits
    .fillna(False)
    .astype(bool)
)

print(entries.dtype)
print(exits.dtype)

print(type(entries))
print(type(exits))

print(entries.head())
print(exits.head())


print(type(data["Close"]))
print(data["Close"].dtype)
print(data["Close"].head())
close = data["Close"].astype(float)

portfolio = vbt.Portfolio.from_signals(
    close=close,
    entries=entries,
    exits=exits,
    init_cash=100000,
    freq="1D"
)
print()
print("Trades:", portfolio.trades.count())
print(
    "Return:",
    portfolio.total_return()
)
print(
    "Sharpe:",
    portfolio.sharpe_ratio()
)
print(
    "Win Rate:",
    portfolio.trades.win_rate()
)
print(
    "Max DD:",
    portfolio.max_drawdown()
)