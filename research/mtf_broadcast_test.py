import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.mtf_context_engine import (
    build_mtf_context
)

from backtesting.mtf_broadcast import (
    broadcast_context
)

# =====================
# DATA
# =====================

data_15m = yf.download(
    "^NSEI",
    period="7d",
    interval="15m"
)

data_5m = yf.download(
    "^NSEI",
    period="7d",
    interval="5m"
)

for df in [data_15m, data_5m]:

    df.columns = (
        df.columns
        .get_level_values(0)
    )

data_15m = compute_features(
    data_15m
)

context = build_mtf_context(
    data_15m
)

broadcasted = broadcast_context(
    context,
    data_5m
)

print()
print("=" * 60)
print("MTF BROADCAST TEST")
print("=" * 60)

print()

print(
    broadcasted.head(20)
)

print()

print(
    "Rows:",
    len(broadcasted)
)

print(
    "Bullish:",
    int(
        broadcasted[
            "BULLISH_CONTEXT"
        ].sum()
    )
)

print(
    "Bearish:",
    int(
        broadcasted[
            "BEARISH_CONTEXT"
        ].sum()
    )
)