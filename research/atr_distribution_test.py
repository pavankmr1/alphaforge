import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

data = yf.download(
    "^NSEI",
    period="30d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

print()
print("=" * 60)
print("ATR DISTRIBUTION")
print("=" * 60)

print(
    data["ATR14"].describe()
)