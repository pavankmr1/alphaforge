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

bullish = context["BULLISH_CONTEXT"]

sweep = data["SWEEP_SWING_LOW"]

rejection = data["LONG_LOWER_WICK"]

confirmation = data["BULLISH_CONFIRMATION"]

print()
print("=" * 60)
print("SWEEP INVESTIGATION")
print("=" * 60)

sweep_indices = sweep[sweep].index[:10]

for idx in sweep_indices:

    pos = data.index.get_loc(idx)

    start = max(0, pos - 5)
    end = min(len(data), pos + 15)

    window = data.iloc[start:end]

    print()
    print("SWEEP:", idx)

    debug = window.copy()

    debug["CONTEXT"] = bullish.loc[window.index]
    debug["SWEEP"] = sweep.loc[window.index]
    debug["REJECTION"] = rejection.loc[window.index]
    debug["CONFIRMATION"] = confirmation.loc[window.index]

    print(
        debug[
            [
                "CONTEXT",
                "SWEEP",
                "REJECTION",
                "CONFIRMATION"
            ]
        ]
    )