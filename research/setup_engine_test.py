import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
)

from backtesting.setup_engine import (
    build_bullish_setup
)

# =====================================
# DATA
# =====================================

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

# =====================================
# CONTEXT
# =====================================

context_df = build_context(data)

bullish_context = (
    context_df["BULLISH_CONTEXT"]
)

# =====================================
# EVENTS
# =====================================

sweep = (
    data["SWEEP_SWING_LOW"]
)

rejection = (
    data["LONG_LOWER_WICK"]
)

confirmation = (
    data["BULLISH_CONFIRMATION"]
)

# =====================================
# SETUP ENGINE
# =====================================

setup = build_bullish_setup(
    context=bullish_context,
    sweep=sweep,
    rejection=rejection,
    confirmation=confirmation
)

# =====================================
# RESULTS
# =====================================

print()
print("=" * 60)
print("SETUP ENGINE TEST")
print("=" * 60)

print(
    "Bullish Context:",
    int(
        bullish_context.sum()
    )
)

print(
    "Liquidity Sweeps:",
    int(
        sweep.sum()
    )
)

print(
    "Rejections:",
    int(
        rejection.sum()
    )
)

print(
    "Confirmations:",
    int(
        confirmation.sum()
    )
)

print(
    "Completed Setups:",
    int(
        setup.sum()
    )
)

print()

print(
    setup[
        setup
    ].index[:20]
)