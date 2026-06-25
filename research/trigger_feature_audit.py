import yfinance as yf
import pandas as pd

from backtesting.feature_engine import compute_features
from backtesting.context_engine import build_context
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

# ==================================
# AUDIT
# ==================================

print()
print("=" * 100)
print("TRIGGER FEATURE AUDIT")
print("=" * 100)

audit = pd.DataFrame({

    "Close": data["Close"],

    "EMA20": data["EMA20"],

    "EMA50": data["EMA50"],

    "BullishContext": context_df[
        "BULLISH_CONTEXT"
    ],

    "BullishStructure": data[
        "BULLISH_STRUCTURE"
    ],

    "Sweep": data[
        "SWEEP_SWING_LOW"
    ],

    "Rejection": data[
        "LONG_LOWER_WICK"
    ],

    "Confirmation": data[
        "BULLISH_CONFIRMATION"
    ],

    "BOS": data[
        "BOS_BULLISH"
    ],

    "StrongBOS": data[
        "STRONG_BOS_BULLISH"
    ],

    "Volume": data[
        "Volume"
    ],

    "ATR14": data[
        "ATR14"
    ]
})

print(
    audit[
        trigger
    ].to_string()
)

print()
print(
    "Triggers:",
    int(trigger.sum())
)