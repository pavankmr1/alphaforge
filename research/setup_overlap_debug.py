import yfinance as yf

from backtesting.feature_engine import compute_features
from backtesting.context_engine import build_context

data = yf.download(
    "^NSEI",
    period="30d",
    interval="15m"
)

data.columns = data.columns.get_level_values(0)

data = compute_features(data)

context = build_context(data)

sweep = data["SWEEP_SWING_LOW"]
rejection = data["LONG_LOWER_WICK"]
confirmation = data["BULLISH_CONFIRMATION"]

print()
print("=" * 60)
print("OVERLAP DEBUG")
print("=" * 60)

print(
    "Sweep + Rejection:",
    int((sweep & rejection).sum())
)

print(
    "Sweep + Confirmation:",
    int((sweep & confirmation).sum())
)

print(
    "Rejection + Confirmation:",
    int((rejection & confirmation).sum())
)

print()

for idx in sweep[sweep].index[:10]:

    pos = data.index.get_loc(idx)

    window = data.iloc[
        max(0, pos-3):pos+10
    ]

    print()
    print("SWEEP:", idx)

    print(
        window[
            [
                "SWEEP_SWING_LOW",
                "LONG_LOWER_WICK",
                "BULLISH_CONFIRMATION"
            ]
        ]
    )