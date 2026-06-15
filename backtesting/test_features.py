import yfinance as yf

from feature_engine import (
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

features = compute_features(
    data
)

print(
    features[
        [
            "EMA5",
            "EMA9",
            "EMA10",
            "EMA15",
            "EMA20",
            "EMA21",
            "EMA50",
            "EMA200",
            "VWAP",
            "ATR14",
            "RSI14",
            "VOL_MA20",
            "PreviousDayHigh",
            "PreviousDayLow",
            "Pivot",
            "Support",
            "Resistance"
        ]
    ].tail()
)