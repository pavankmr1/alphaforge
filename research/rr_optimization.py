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
# RR TESTS
# ==================================

rr_tests = [

    ("1:1", 2, 2),
    ("1:2", 2, 4),
    ("1:3", 2, 6)

]

results = []

for rr_name, stop_mult, target_mult in rr_tests:

    exits = pd.Series(
        False,
        index=data.index
    )

    in_trade = False

    stop_price = None
    target_price = None

    for i in range(len(data)):

        if entries.iloc[i] and not in_trade:

            entry_price = (
                data["Close"].iloc[i]
            )

            atr = (
                data["ATR14"].iloc[i]
            )

            stop_price = (
                entry_price
                -
                stop_mult * atr
            )

            target_price = (
                entry_price
                +
                target_mult * atr
            )

            in_trade = True

        elif in_trade:

            low = data["Low"].iloc[i]
            high = data["High"].iloc[i]

            stop_hit = (
                low <= stop_price
            )

            target_hit = (
                high >= target_price
            )

            if stop_hit or target_hit:

                exits.iloc[i] = True

                in_trade = False

                stop_price = None
                target_price = None

    portfolio = vbt.Portfolio.from_signals(

        close=data["Close"],

        entries=entries,

        exits=exits,

        init_cash=100000,

        freq="15m"

    )

    results.append({

        "RR": rr_name,

        "Trades": int(
            portfolio.trades.count()
        ),

        "Return": round(
            float(
                portfolio.total_return()
            ),
            4
        ),

        "Sharpe": round(
            float(
                portfolio.sharpe_ratio()
            ),
            4
        ),

        "WinRate": round(
            float(
                portfolio.trades.win_rate()
            ),
            4
        ),

        "MaxDD": round(
            float(
                portfolio.max_drawdown()
            ),
            4
        )

    })

# ==================================
# REPORT
# ==================================

report = pd.DataFrame(
    results
)

print()
print("=" * 80)
print("RR OPTIMIZATION")
print("=" * 80)
print()

print(report)

print()

best_sharpe = report.loc[
    report["Sharpe"].idxmax()
]

print("=" * 80)
print("BEST SHARPE")
print("=" * 80)

print(best_sharpe)

print()

best_return = report.loc[
    report["Return"].idxmax()
]

print("=" * 80)
print("BEST RETURN")
print("=" * 80)

print(best_return)