import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.mtf_context_engine import (
    build_mtf_context
)

# ==========================
# 15M DATA
# ==========================

data_15m = yf.download(
    "^NSEI",
    period="7d",
    interval="15m"
)

data_15m.columns = (
    data_15m.columns
    .get_level_values(0)
)

data_15m = compute_features(
    data_15m
)

context = build_mtf_context(
    data_15m
)

print()
print("=" * 60)
print("MTF CONTEXT TEST")
print("=" * 60)

print()

print(
    "Bullish:",
    int(
        context[
            "BULLISH_CONTEXT"
        ].sum()
    )
)

print(
    "Bearish:",
    int(
        context[
            "BEARISH_CONTEXT"
        ].sum()
    )
)

print()

print(
    context.tail(20)
)