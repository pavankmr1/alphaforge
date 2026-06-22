import yfinance as yf
import vectorbt as vbt
import pandas as pd

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
)

from backtesting.scoring_engine import (
    bullish_score
)

# ==================================
# DATA
# ==================================

data = yf.download(
    "^NSEI",
    period="60d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

context = build_context(data)

score = bullish_score(
    data,
    context
)

# ==================================
# ENTRY
# ==================================

recent_sweep = (

    data["SWEEP_SWING_LOW"]

    .rolling(5)

    .max()

    .fillna(False)

    .astype(bool)

)

entries = (

    (score >= 8)

    &

    recent_sweep

)

# ==================================
# EXIT
# ==================================

exits = (
    data["BOS_BEARISH"]
)

# ==================================
# BACKTEST
# ==================================

portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=entries,

    exits=exits,

    init_cash=100000,

    freq="15m"

)

# ==================================
# TRADE AUDIT
# ==================================

trades = (
    portfolio.trades
    .records_readable
)

audit = pd.DataFrame({

    "Entry": trades[
        "Entry Timestamp"
    ],

    "Exit": trades[
        "Exit Timestamp"
    ],

    "Return": trades[
        "Return"
    ]

})

audit = audit.sort_values(
    by="Return"
)

print()
print("=" * 100)
print("TRADE PERIOD AUDIT")
print("=" * 100)

print(audit)

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print()

print(
    audit["Return"]
    .describe()
)

print()

print(
    "Worst Trade:",
    round(
        audit["Return"]
        .min(),
        4
    )
)

print(
    "Best Trade:",
    round(
        audit["Return"]
        .max(),
        4
    )
)

print(
    "Total Trades:",
    len(audit)
)