import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = data.columns.get_level_values(0)

data = compute_features(data)

features = [
    "BULLISH_TREND_V2",
    "SWEEP_SWING_LOW",
    "BULLISH_SWEEP_REJECTION",
    "BOS_BULLISH",
    "STRONG_BOS_BULLISH",
    "BULLISH_CONFIRMATION"
]

print()
print("=" * 60)
print("FEATURE FREQUENCY")
print("=" * 60)

for f in features:

    print(
        f,
        int(data[f].sum())
    )