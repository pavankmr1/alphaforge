import yfinance as yf

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

data = compute_features(data)

swing_high = (
    (data["High"] > data["High"].shift(1))
    &
    (data["High"] > data["High"].shift(-1))
)

swing_low = (
    (data["Low"] < data["Low"].shift(1))
    &
    (data["Low"] < data["Low"].shift(-1))
)

print()
print("=" * 60)
print("SWING DETECTION")
print("=" * 60)

print("Swing Highs:", int(swing_high.sum()))
print("Swing Lows:", int(swing_low.sum()))