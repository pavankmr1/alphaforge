import yfinance as yf

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

# ----------------------------------
# Candidate Setup
# ----------------------------------

sweep = data["SWEEP_SWING_LOW"]

rejection = data["LONG_LOWER_WICK"]

confirmation = data["BULLISH_CONFIRMATION"]

state = 0

candidate_setup = sweep.copy()

candidate_setup[:] = False

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

# ----------------------------------
# Qualification
# ----------------------------------

qualified = qualify_bullish_setup(

    candidate_setup,

    context_df["BULLISH_CONTEXT"],

    data["BULLISH_STRUCTURE"]

)

# ----------------------------------
# Trigger
# ----------------------------------

trigger = bullish_trigger(

    qualified,

    data["BOS_BULLISH"]

)

print()
print("=" * 60)
print("TRIGGER ENGINE")
print("=" * 60)

print(
    "Candidate:",
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

print()

print(
    trigger[
        trigger
    ].index[:20]
)