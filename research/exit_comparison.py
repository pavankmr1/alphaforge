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
# EXIT A
# CURRENT BOS EXIT
# ==================================

bos_portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=entries,

    exits=data["BOS_BEARISH"],

    init_cash=100000,

    freq="15m"

)

# ==================================
# EXIT B
# 2 ATR STOP
# ==================================

atr_stop = (

    data["Close"]

    - 2 * data["ATR14"]

)

atr_entries = entries.copy()

atr_exits = pd.Series(
    False,
    index=data.index
)

in_trade = False
stop_price = None

for i in range(len(data)):

    if atr_entries.iloc[i] and not in_trade:

        in_trade = True

        stop_price = (
            data["Close"].iloc[i]
            -
            2 * data["ATR14"].iloc[i]
        )

    elif in_trade:

        if data["Low"].iloc[i] <= stop_price:

            atr_exits.iloc[i] = True

            in_trade = False

            stop_price = None

atr_portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=atr_entries,

    exits=atr_exits,

    init_cash=100000,

    freq="15m"

)

# ==================================
# REPORT
# ==================================

results = pd.DataFrame({

    "Strategy": [
        "BOS Exit",
        "ATR 2x Stop"
    ],

    "Trades": [

        int(
            bos_portfolio.trades.count()
        ),

        int(
            atr_portfolio.trades.count()
        )

    ],

    "Return": [

        round(
            float(
                bos_portfolio.total_return()
            ),
            4
        ),

        round(
            float(
                atr_portfolio.total_return()
            ),
            4
        )

    ],

    "Sharpe": [

        round(
            float(
                bos_portfolio.sharpe_ratio()
            ),
            4
        ),

        round(
            float(
                atr_portfolio.sharpe_ratio()
            ),
            4
        )

    ],

    "WinRate": [

        round(
            float(
                bos_portfolio.trades.win_rate()
            ),
            4
        ),

        round(
            float(
                atr_portfolio.trades.win_rate()
            ),
            4
        )

    ],

    "MaxDD": [

        round(
            float(
                bos_portfolio.max_drawdown()
            ),
            4
        ),

        round(
            float(
                atr_portfolio.max_drawdown()
            ),
            4
        )

    ]

})

print()
print("=" * 80)
print("EXIT COMPARISON")
print("=" * 80)
print()
print(results)