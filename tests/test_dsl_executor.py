import yfinance as yf

from backtesting.feature_engine import (
    compute_features
)

from backtesting.dsl_executor import (
    execute_rule
)

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = data.columns.get_level_values(0)

data = compute_features(data)

rule = {

    "type": "cross_above",

    "left": "EMA9",

    "right": "EMA20"
}

signal = execute_rule(
    rule,
    data
)

print(
    signal.sum()
)