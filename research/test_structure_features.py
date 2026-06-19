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

features = [

    "HIGHER_HIGH",
    "HIGHER_LOW",
    "LOWER_HIGH",
    "LOWER_LOW",
    "BULLISH_STRUCTURE",
    "BEARISH_STRUCTURE"

]

for feature in features:

    print()
    print(feature)

    print(
        data[feature]
        .value_counts()
    )