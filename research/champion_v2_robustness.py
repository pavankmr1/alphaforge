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

periods = [
    "15d",
    "30d",
    "60d"
]

results = []

for period in periods:

    print()
    print("=" * 60)
    print(f"RUNNING {period}")
    print("=" * 60)

    data = yf.download(
        "^NSEI",
        period=period,
        interval="15m"
    )

    if data.empty:
        continue

    data.columns = (
        data.columns
        .get_level_values(0)
    )

    data = compute_features(
        data
    )

    context = build_context(
        data
    )

    score = bullish_score(
        data,
        context
    )

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

    # ==========================
    # ATR RR EXIT (1:3)
    # ==========================

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
                2 * atr
            )

            target_price = (
                entry_price
                +
                6 * atr
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

        "Period": period,

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

report = pd.DataFrame(
    results
)

print()
print("=" * 80)
print("ALPHAFORGE CHAMPION V2 ROBUSTNESS")
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