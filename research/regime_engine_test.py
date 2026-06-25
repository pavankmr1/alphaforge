import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.regime_engine import (
    build_regime
)

data = yf.download(
    "^NSEI",
    period="60d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(
    data
)

regime = build_regime(
    data
)

print()
print("=" * 60)
print("REGIME ENGINE")
print("=" * 60)

print(
    "Trending:",
    int(
        regime[
            "TRENDING"
        ].sum()
    )
)

print(
    "Ranging:",
    int(
        regime[
            "RANGING"
        ].sum()
    )
)

print()

print(
    regime.tail(20)
)