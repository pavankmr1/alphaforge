import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.state_engine import (
    sequence_signal
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

trend = (
    data["EMA20"]
    >
    data["EMA50"]
)

liquidity = (
    data["Low"]
    <
    data["LiquidityLow"].shift(1)
)

confirmation = (
    data["BULLISH_CONFIRMATION"]
)

signals = sequence_signal(
    trend,
    liquidity,
    confirmation,
    lookahead=5
)

print()
print("=" * 60)
print("STATE ENGINE TEST")
print("=" * 60)

print(
    "Trend:",
    int(trend.sum())
)

print(
    "Liquidity:",
    int(liquidity.sum())
)

print(
    "Confirmation:",
    int(confirmation.sum())
)

print(
    "Sequence Signals:",
    int(signals.sum())
)

print()

print(
    signals[
        signals
    ].index
)