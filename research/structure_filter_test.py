import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

# ==================================
# DATA
# ==================================

data = yf.download(
    "^NSEI",
    start="2024-01-01",
    end="2025-01-01"
)

data.columns = (
    data.columns
    .get_level_values(0)
)

data = compute_features(data)

# ==================================
# ORIGINAL CROSS
# EMA21 crosses above EMA9
# ==================================

cross_above = (

    (data["EMA21"] > data["EMA9"])

    &

    (
        data["EMA21"].shift(1)
        <=
        data["EMA9"].shift(1)
    )

)

# ==================================
# BULLISH CROSS
# EMA9 crosses above EMA21
# ==================================

bullish_cross = (

    (data["EMA9"] > data["EMA21"])

    &

    (
        data["EMA9"].shift(1)
        <=
        data["EMA21"].shift(1)
    )

)

# ==================================
# EXIT
# ==================================

cross_below = (

    (data["EMA9"] < data["EMA21"])

    &

    (
        data["EMA9"].shift(1)
        >=
        data["EMA21"].shift(1)
    )

)

# ==================================
# FILTERED SIGNALS
# ==================================

filtered_entries = (

    bullish_cross

    &

    data["BULLISH_STRUCTURE"]

)

filtered_entries = (
    filtered_entries
    .fillna(False)
    .astype(bool)
)

filtered_exits = (
    cross_below
    .shift(1)
    .fillna(False)
    .astype(bool)
)

close = (
    data["Close"]
    .astype(float)
)

# ==================================
# DIAGNOSTICS
# ==================================

print()
print("=" * 60)
print("CROSSOVER ANALYSIS")
print("=" * 60)

print()

print(
    "EMA21 Cross Above EMA9:",
    int(cross_above.sum())
)

print(
    "EMA9 Cross Above EMA21:",
    int(bullish_cross.sum())
)

print(
    "Bullish Structure:",
    int(
        data["BULLISH_STRUCTURE"].sum()
    )
)

print(
    "Bullish Cross + Structure:",
    int(
        (
            bullish_cross
            &
            data["BULLISH_STRUCTURE"]
        ).sum()
    )
)

print()

print("=" * 60)
print("BULLISH CROSS ROWS")
print("=" * 60)

print()

print(
    data.loc[
        bullish_cross,
        [
            "Close",
            "EMA9",
            "EMA21",
            "HIGHER_HIGH",
            "HIGHER_LOW",
            "BULLISH_STRUCTURE"
        ]
    ]
)

# ==================================
# BACKTEST
# ==================================

portfolio = vbt.Portfolio.from_signals(
    close=close,
    entries=filtered_entries,
    exits=filtered_exits,
    init_cash=100000,
    freq="1D"
)

print()
print("=" * 60)
print("EMA BULLISH CROSS + STRUCTURE")
print("=" * 60)

print(
    "Signals:",
    int(filtered_entries.sum())
)

print(
    "Trades:",
    portfolio.trades.count()
)

print(
    "Return:",
    round(
        float(
            portfolio.total_return()
        ),
        4
    )
)

print(
    "Sharpe:",
    round(
        float(
            portfolio.sharpe_ratio()
        ),
        4
    )
)

print(
    "Win Rate:",
    round(
        float(
            portfolio.trades.win_rate()
        ),
        4
    )
)

print(
    "Max DD:",
    round(
        float(
            portfolio.max_drawdown()
        ),
        4
    )
)