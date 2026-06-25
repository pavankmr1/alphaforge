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

from backtesting.mtf_setup_engine import (
    build_5m_setup
)

# ==========================
# DATA
# ==========================

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

data_5m = compute_features(
    data_5m
)

# ==========================
# CONTEXT
# ==========================

context_15m = build_mtf_context(
    data_15m
)

context_5m = broadcast_context(
    context_15m,
    data_5m
)

# ==========================
# SETUPS
# ==========================

setups = build_5m_setup(
    data_5m,
    context_5m
)

print()
print("=" * 60)
print("MTF SETUP TEST")
print("=" * 60)

print()

print(
    "Bullish Context 5m:",
    int(
        context_5m["BULLISH_CONTEXT"].sum()
    )
)

print(
    "Setups:",
    int(
        setups.sum()
    )
)

print()

print(
    setups[
        setups
    ].index[:20]
)

print()
print("=" * 60)
print("COMPONENT COUNTS")
print("=" * 60)

print(
    "Bullish Context:",
    int(
        context_5m["BULLISH_CONTEXT"].sum()
    )
)

print(
    "Sweep:",
    int(
        data_5m["SWEEP_SWING_LOW"].sum()
    )
)

print(
    "BOS Bullish:",
    int(
        data_5m["BOS_BULLISH"].sum()
    )
)