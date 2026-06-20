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
print("BOS TEST")
print("=" * 60)

print(
    "Bullish BOS:",
    int(
        data["BOS_BULLISH"].sum()
    )
)

print(
    "Bearish BOS:",
    int(
        data["BOS_BEARISH"].sum()
    )
)

print()

print(
    data.loc[
        data["BOS_BULLISH"],
        ["Close", "LAST_SWING_HIGH"]
    ].head(10)
)