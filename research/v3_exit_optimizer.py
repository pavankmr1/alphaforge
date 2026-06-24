import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

# ==================================
# LOAD DATA
# ==================================

data = pd.read_csv(
    "data/processed/nifty_15m_master.csv"
)

data["datetime"] = pd.to_datetime(
    data["datetime"]
)

data.set_index(
    "datetime",
    inplace=True
)

data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    },
    inplace=True
)

data = compute_features(data)

# ==================================
# V3 ENTRY
# ==================================

bullish_trend = (

    data["EMA20"]

    >

    data["EMA50"]

)

recent_sweep = (

    data["SWEEP_SWING_LOW"]

    .rolling(5)

    .max()

    .fillna(False)

    .astype(bool)

)

bullish_mss = (

    data["BOS_BULLISH"]

)

entries = (

    bullish_trend

    &

    recent_sweep

    &

    bullish_mss

)

# ==================================
# EXIT TESTER
# ==================================

atr_targets = [

    1,
    2,
    3,
    4

]

results = []

for rr in atr_targets:

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
                atr
            )

            target_price = (
                entry_price
                +
                (rr * atr)
            )

            in_trade = True

        elif in_trade:

            low = (
                data["Low"].iloc[i]
            )

            high = (
                data["High"].iloc[i]
            )

            stop_hit = (
                low <= stop_price
            )

            target_hit = (
                high >= target_price
            )

            if stop_hit or target_hit:

                exits.iloc[i] = True

                in_trade = False

    portfolio = vbt.Portfolio.from_signals(

        close=data["Close"],

        entries=entries,

        exits=exits,

        init_cash=100000,

        freq="15m"

    )

    results.append({

        "RR": f"1:{rr}",

        "Trades":
            portfolio.trades.count(),

        "Return":
            round(
                float(
                    portfolio.total_return()
                ),
                4
            ),

        "Sharpe":
            round(
                float(
                    portfolio.sharpe_ratio()
                ),
                4
            ),

        "WinRate":
            round(
                float(
                    portfolio.trades.win_rate()
                ),
                4
            ),

        "MaxDD":
            round(
                float(
                    portfolio.max_drawdown()
                ),
                4
            )
    })

# ==================================
# REPORT
# ==================================

results_df = pd.DataFrame(
    results
)

print()
print("=" * 80)
print("V3 EXIT OPTIMIZER")
print("=" * 80)

print(results_df)