import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
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

context = build_context(data)

print()
print("=" * 60)
print("CONTEXT ENGINE")
print("=" * 60)

print(
    "Bullish:",
    int(
        context["BULLISH_CONTEXT"].sum()
    )
)

print(
    "Bearish:",
    int(
        context["BEARISH_CONTEXT"].sum()
    )
)

print(
    "Range:",
    int(
        context["RANGE_CONTEXT"].sum()
    )
)