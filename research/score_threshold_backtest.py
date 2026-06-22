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

score = bullish_score(
    data,
    context
)

# ==================================
# THRESHOLD TESTING
# ==================================

results = []

thresholds = [6, 7, 8]

for threshold in thresholds:

    entries = (
        score >= threshold
    )

    exits = (
        data["BOS_BEARISH"]
    )

    portfolio = vbt.Portfolio.from_signals(

        close=data["Close"],

        entries=entries,

        exits=exits,

        init_cash=100000,

        freq="15m"

    )

    results.append({

        "Threshold": threshold,

        "Signals": int(
            entries.sum()
        ),

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
print("ALPHAFORGE SCORE THRESHOLD TEST")
print("=" * 80)

print()
print(report)

print()

best_return = report.loc[
    report["Return"].idxmax()
]

print("=" * 80)
print("BEST RETURN")
print("=" * 80)

print(best_return)

print()

best_sharpe = report.loc[
    report["Sharpe"].idxmax()
]

print("=" * 80)
print("BEST SHARPE")
print("=" * 80)

print(best_sharpe)