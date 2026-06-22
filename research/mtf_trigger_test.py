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

from backtesting.mtf_trigger_engine import (
    build_1m_trigger
)

# ==================================================
# DOWNLOAD DATA
# ==================================================

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

data_1m = yf.download(
    "^NSEI",
    period="7d",
    interval="1m"
)

# ==================================================
# FLATTEN COLUMNS
# ==================================================

for df in [
    data_15m,
    data_5m,
    data_1m
]:

    df.columns = (
        df.columns
        .get_level_values(0)
    )

# ==================================================
# FEATURES
# ==================================================

data_15m = compute_features(
    data_15m
)

data_5m = compute_features(
    data_5m
)

data_1m = compute_features(
    data_1m
)

# ==================================================
# 15M CONTEXT
# ==================================================

context_15m = build_mtf_context(
    data_15m
)

# ==================================================
# BROADCAST 15M -> 5M
# ==================================================

context_5m = broadcast_context(
    context_15m,
    data_5m
)

# ==================================================
# 5M SETUPS
# ==================================================

setup_5m = build_5m_setup(
    data_5m,
    context_5m
)

# ==================================================
# BROADCAST 5M -> 1M
# ==================================================

setup_1m = (

    setup_5m

    .reindex(
        data_1m.index,
        method="ffill"
    )

    .fillna(False)

    .astype(bool)

)

# ==================================================
# 1M TRIGGERS
# ==================================================

triggers = build_1m_trigger(
    data_1m,
    setup_1m
)

# ==================================================
# REPORT
# ==================================================

print()
print("=" * 60)
print("MTF TRIGGER TEST")
print("=" * 60)

print()

print(
    "15M Bullish Context:",
    int(
        context_15m[
            "BULLISH_CONTEXT"
        ].sum()
    )
)

print(
    "5M Bullish Context:",
    int(
        context_5m[
            "BULLISH_CONTEXT"
        ].sum()
    )
)

print(
    "5M Setups:",
    int(
        setup_5m.sum()
    )
)

print(
    "1M Setup Broadcast:",
    int(
        setup_1m.sum()
    )
)

print(
    "1M Triggers:",
    int(
        triggers.sum()
    )
)

print()

print("=" * 60)
print("FIRST 20 TRIGGERS")
print("=" * 60)

print()

print(
    triggers[
        triggers
    ].index[:20]
)

print()

print("=" * 60)
print("LAST 20 TRIGGERS")
print("=" * 60)

print()

print(
    triggers[
        triggers
    ].index[-20:]
)