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

print()
print("=" * 60)
print("STRONG BOS TEST")
print("=" * 60)

print(
    "BOS Bullish:",
    int(data["BOS_BULLISH"].sum())
)

print(
    "Strong BOS Bullish:",
    int(data["STRONG_BOS_BULLISH"].sum())
)

print(
    "BOS Bearish:",
    int(data["BOS_BEARISH"].sum())
)

print(
    "Strong BOS Bearish:",
    int(data["STRONG_BOS_BEARISH"].sum())
)