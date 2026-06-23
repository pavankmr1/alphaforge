import pandas as pd
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
# DATA
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

for df in [
    data_15m,
    data_5m,
    data_1m
]:
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

data_1m = compute_features(
    data_1m
)

# ==================================================
# CONTEXT
# ==================================================

context_15m = build_mtf_context(
    data_15m
)

context_5m = broadcast_context(
    context_15m,
    data_5m
)

# ==================================================
# SETUP
# ==================================================

setup_5m = build_5m_setup(
    data_5m,
    context_5m
)

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
# TRIGGERS
# ==================================================

triggers = build_1m_trigger(
    data_1m,
    setup_1m
)

# ==================================================
# DEBUG TRIGGERS
# ==================================================

trigger_times = (
    data_1m[
        triggers
    ].index
)

print()
print("=" * 80)
print("MTF TRADE DEBUG")
print("=" * 80)

for idx, ts in enumerate(trigger_times):

    close = (
        data_1m.loc[
            ts,
            "Close"
        ]
    )

    atr = (
        data_1m.loc[
            ts,
            "ATR14"
        ]
    )

    stop = (
        close
        -
        2 * atr
    )

    target = (
        close
        +
        6 * atr
    )

    rr_points = (
        target
        -
        close
    )

    print()
    print("-" * 80)

    print(
        f"TRIGGER #{idx+1}"
    )

    print(
        "Time:",
        ts.tz_convert(
            "Asia/Kolkata"
        )
    )

    print(
        "Close:",
        round(float(close), 2)
    )

    print(
        "ATR:",
        round(float(atr), 2)
    )

    print(
        "Stop:",
        round(float(stop), 2)
    )

    print(
        "Target:",
        round(float(target), 2)
    )

    print(
        "Target Distance:",
        round(float(rr_points), 2)
    )