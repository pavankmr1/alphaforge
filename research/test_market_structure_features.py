import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(
    data
)

print()

features = [

    "CONSEC_GREEN_3",

    "LONG_LOWER_WICK",

    "BULLISH_CONFIRMATION",

    "PREV_BEARISH_HIGH",

    "PREV_BEARISH_LOW"

]

for feature in features:

    print()

    print(
        feature
    )

    print(
        data[feature]
        .value_counts()
        .head()
    )