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
    period="30d",
    interval="15m"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

context = build_context(data)

# ==================================
# SCORE
# ==================================

score = bullish_score(
    data,
    context
)

entries = (
    score >= 8
)

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

print()
print("=" * 100)
print("ELITE TRADE AUDIT")
print("=" * 100)

trades = portfolio.trades.records_readable

for idx, trade in trades.iterrows():

    entry_time = trade["Entry Timestamp"]

    entry_row = data.loc[entry_time]

    print()
    print("-" * 100)

    print(
        f"TRADE #{idx + 1}"
    )

    print(
        "Entry:",
        entry_time
    )

    print(
        "Return:",
        round(
            float(
                trade["Return"]
            ),
            4
        )
    )

    print()

    print(
        "Close:",
        round(
            float(
                entry_row["Close"]
            ),
            2
        )
    )

    print(
        "ATR14:",
        round(
            float(
                entry_row["ATR14"]
            ),
            2
        )
    )

    print(
        "Score:",
        int(
            score.loc[
                entry_time
            ]
        )
    )

    print()

    print(
        "Bullish Context:",
        bool(
            context[
                "BULLISH_CONTEXT"
            ].loc[
                entry_time
            ]
        )
    )

    print(
        "Bullish Structure:",
        bool(
            entry_row[
                "BULLISH_STRUCTURE"
            ]
        )
    )

    print(
        "Strong BOS:",
        bool(
            entry_row[
                "STRONG_BOS_BULLISH"
            ]
        )
    )

    print(
        "Confirmation:",
        bool(
            entry_row[
                "BULLISH_CONFIRMATION"
            ]
        )
    )

    print(
        "Sweep:",
        bool(
            entry_row[
                "SWEEP_SWING_LOW"
            ]
        )
    )

print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)

print(
    "Trades:",
    portfolio.trades.count()
)

print(
    "Return:",
    round(
        float(
            portfolio.total_return()
        ),
        4
    )
)

print(
    "Sharpe:",
    round(
        float(
            portfolio.sharpe_ratio()
        ),
        4
    )
)

print(
    "Win Rate:",
    round(
        float(
            portfolio.trades.win_rate()
        ),
        4
    )
)