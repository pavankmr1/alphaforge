import yfinance as yf
import vectorbt as vbt
import pandas as pd

from backtesting.feature_engine import compute_features
from backtesting.context_engine import build_context
from backtesting.qualification_engine import qualify_bullish_setup
from backtesting.trigger_engine import bullish_trigger

# ==================================
# DATA
# ==================================

data = yf.download(
    "^NSEI",
    period="30d",
    interval="15m"
)

data.columns = data.columns.get_level_values(0)

data = compute_features(data)

context_df = build_context(data)

# ==================================
# SETUP
# ==================================

sweep = data["SWEEP_SWING_LOW"]
rejection = data["LONG_LOWER_WICK"]
confirmation = data["BULLISH_CONFIRMATION"]

candidate_setup = pd.Series(
    False,
    index=data.index
)

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

exit_signal = data["BOS_BEARISH"]

portfolio = vbt.Portfolio.from_signals(

    close=data["Close"],

    entries=trigger,

    exits=exit_signal,

    init_cash=100000,

    freq="15m"
)

# ==================================
# TRADE AUDIT
# ==================================

print()
print("=" * 80)
print("TRADE AUDIT")
print("=" * 80)

trades = portfolio.trades.records_readable

print(trades)