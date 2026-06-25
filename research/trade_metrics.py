import yfinance as yf
import vectorbt as vbt
import pandas as pd

from backtesting.feature_engine import compute_features
from backtesting.context_engine import build_context
from backtesting.scoring_engine import bullish_score

# ==========================
# DATA
# ==========================

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
# ATR RR EXIT
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

        entry_price = data["Close"].iloc[i]
        atr = data["ATR14"].iloc[i]

        stop_price = (
            entry_price
            - 2 * atr
        )

        target_price = (
            entry_price
            + 6 * atr
        )

        in_trade = True

    elif in_trade:

        low = data["Low"].iloc[i]
        high = data["High"].iloc[i]

        if (
            low <= stop_price
            or
            high >= target_price
        ):

            exits.iloc[i] = True

            in_trade = False

# ==========================
# BACKTEST
# ==========================

portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=entries,

    exits=exits,

    init_cash=100000,

    freq="15m"

)

# ==========================
# TRADE METRICS
# ==========================

trades = (
    portfolio.trades
    .records_readable
)

returns = trades["Return"]

wins = returns[
    returns > 0
]

losses = returns[
    returns < 0
]

profit_factor = (
    wins.sum()
    /
    abs(losses.sum())
)

expectancy = returns.mean()

print()
print("=" * 80)
print("ALPHAFORGE TRADE METRICS")
print("=" * 80)

print()

print(
    "Trades:",
    len(returns)
)

print(
    "Profit Factor:",
    round(profit_factor, 4)
)

print(
    "Expectancy:",
    round(expectancy, 4)
)

print(
    "Average Winner:",
    round(wins.mean(), 4)
)

print(
    "Average Loser:",
    round(losses.mean(), 4)
)

print(
    "Largest Winner:",
    round(wins.max(), 4)
)

print(
    "Largest Loser:",
    round(losses.min(), 4)
)

print(
    "Win Rate:",
    round(
        len(wins)
        /
        len(returns),
        4
    )
)