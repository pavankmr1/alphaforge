import yfinance as yf

from backtesting.feature_engine import compute_features
from backtesting.context_engine import build_context

data = yf.download(
    "^NSEI",
    period="30d",
    interval="15m"
)

data.columns = data.columns.get_level_values(0)

data = compute_features(data)

context = build_context(data)

print()

bullish = context["BULLISH_CONTEXT"]

print(
    data[
        bullish
    ][
        [
            "Close",
            "EMA20",
            "EMA50"
        ]
    ].head(20)
)

print()

print(
    "Bullish Count:",
    bullish.sum()
)