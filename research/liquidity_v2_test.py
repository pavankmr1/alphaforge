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
print("=" * 60)
print("LIQUIDITY V3")
print("=" * 60)

print(
    "Swing Low Sweeps:",
    int(
        data[
            "SWEEP_SWING_LOW"
        ].sum()
    )
)

print(
    "Swing High Sweeps:",
    int(
        data[
            "SWEEP_SWING_HIGH"
        ].sum()
    )
)

print()

print(
    data.loc[
        data["SWEEP_SWING_LOW"],
        ["Close", "LAST_SWING_LOW"]
    ].head(10)
)

print()

print(
    data.loc[
        data["SWEEP_SWING_HIGH"],
        ["Close", "LAST_SWING_HIGH"]
    ].head(10)
)