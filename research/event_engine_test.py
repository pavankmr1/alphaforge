import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.event_engine import (
    event_followed_by
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

liquidity = (

    data["Low"]

    <

    data["LiquidityLow"].shift(1)

)

confirmation = (
    data["BULLISH_CONFIRMATION"]
)

signals = event_followed_by(
    liquidity,
    confirmation,
    lookahead=3
)

print()
print("=" * 60)
print("EVENT ENGINE TEST")
print("=" * 60)

print(
    "Liquidity Events:",
    int(liquidity.sum())
)

print(
    "Confirmation Events:",
    int(confirmation.sum())
)

print(
    "Sequential Signals:",
    int(signals.sum())
)

print()

print(
    signals[
        signals
    ].index
)