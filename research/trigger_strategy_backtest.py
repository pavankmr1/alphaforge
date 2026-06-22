import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

from backtesting.context_engine import (
    build_context
)

from backtesting.qualification_engine import (
    qualify_bullish_setup
)

from backtesting.trigger_engine import (
    bullish_trigger
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

context_df = build_context(data)

# ==================================
# SETUP ENGINE
# ==================================

sweep = data["SWEEP_SWING_LOW"]

rejection = data["LONG_LOWER_WICK"]

confirmation = data["BULLISH_CONFIRMATION"]

candidate_setup = sweep.copy()

candidate_setup[:] = False

state = 0

for i in range(len(data)):

    if state == 0:

        if sweep.iloc[i]:
            state = 1

    elif state == 1:

        if rejection.iloc[i]:
            state = 2

    elif state == 2:

        if confirmation.iloc[i]:

            candidate_setup.iloc[i] = True

            state = 0

# ==================================
# QUALIFICATION
# ==================================

qualified = qualify_bullish_setup(

    candidate_setup,

    context_df["BULLISH_CONTEXT"],

    data["BULLISH_STRUCTURE"]

)

# ==================================
# TRIGGER
# ==================================

trigger = bullish_trigger(

    qualified,

    data["BOS_BULLISH"]

)

# ==================================
# EXIT LOGIC
# ==================================

exit_signal = (

    data["BOS_BEARISH"]

)

# ==================================
# BACKTEST
# ==================================

portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=trigger,

    exits=exit_signal,

    init_cash=100000,

    freq="15m"

)

print()
print("=" * 60)
print("ALPHAFORGE V1")
print("=" * 60)

print(
    "Candidates:",
    int(candidate_setup.sum())
)

print(
    "Qualified:",
    int(qualified.sum())
)

print(
    "Triggered:",
    int(trigger.sum())
)

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

print(
    "Max DD:",
    round(
        float(
            portfolio.max_drawdown()
        ),
        4
    )
)