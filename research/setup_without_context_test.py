import yfinance as yf

from backtesting.feature_engine import (
    compute_features
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

sweep = data["SWEEP_SWING_LOW"]

rejection = data["LONG_LOWER_WICK"]

confirmation = data["BULLISH_CONFIRMATION"]

state = 0

signals = 0

for i in range(len(data)):

    if state == 0:

        if sweep.iloc[i]:
            state = 1

    elif state == 1:

        if rejection.iloc[i]:
            state = 2

    elif state == 2:

        if confirmation.iloc[i]:

            signals += 1

            state = 0

print()
print("=" * 60)
print("SETUP WITHOUT CONTEXT")
print("=" * 60)

print(
    "Sweeps:",
    int(sweep.sum())
)

print(
    "Rejections:",
    int(rejection.sum())
)

print(
    "Confirmations:",
    int(confirmation.sum())
)

print()
print(
    "Completed Setups:",
    signals
)