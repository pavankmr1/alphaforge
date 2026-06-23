import pandas as pd
import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

from backtesting.mtf_context_engine import (
    build_mtf_context
)

from backtesting.mtf_broadcast import (
    broadcast_context
)

from backtesting.mtf_setup_engine import (
    build_5m_setup
)

from backtesting.mtf_trigger_engine import (
    build_1m_trigger
)

# ==================================================
# DOWNLOAD DATA
# ==================================================

print()
print("=" * 60)
print("DOWNLOADING DATA")
print("=" * 60)

data_15m = yf.download(
    "^NSEI",
    period="7d",
    interval="15m"
)

data_5m = yf.download(
    "^NSEI",
    period="7d",
    interval="5m"
)

data_1m = yf.download(
    "^NSEI",
    period="7d",
    interval="1m"
)

for df in [
    data_15m,
    data_5m,
    data_1m
]:

    df.columns = (
        df.columns
        .get_level_values(0)
    )

# ==================================================
# FEATURES
# ==================================================

data_15m = compute_features(
    data_15m
)

data_5m = compute_features(
    data_5m
)

data_1m = compute_features(
    data_1m
)

# ==================================================
# 15M CONTEXT
# ==================================================

context_15m = build_mtf_context(
    data_15m
)

# ==================================================
# 15M -> 5M
# ==================================================

context_5m = broadcast_context(
    context_15m,
    data_5m
)

# ==================================================
# 5M SETUPS
# ==================================================

setup_5m = build_5m_setup(
    data_5m,
    context_5m
)

# ==================================================
# 5M -> 1M
# ==================================================

setup_1m = (

    setup_5m

    .reindex(
        data_1m.index,
        method="ffill"
    )

    .fillna(False)

    .astype(bool)

)

# ==================================================
# 1M TRIGGERS
# ==================================================

entries = build_1m_trigger(
    data_1m,
    setup_1m
)

# ==================================================
# TRAILING STOP EXIT ENGINE
# ==================================================

exits = pd.Series(
    False,
    index=data_1m.index
)

in_trade = False

entry_atr = None
highest_price = None
trail_stop = None

for i in range(len(data_1m)):

    current_time = (
        data_1m.index[i]
        .tz_convert("Asia/Kolkata")
    )

    # ENTRY

    if entries.iloc[i] and not in_trade:

        entry_price = (
            data_1m["Close"].iloc[i]
        )

        entry_atr = (
            data_1m["ATR14"].iloc[i]
        )

        highest_price = entry_price

        trail_stop = (

            entry_price

            -

            (2 * entry_atr)

        )

        in_trade = True

    # MANAGE OPEN POSITION

    elif in_trade:

        high = (
            data_1m["High"].iloc[i]
        )

        low = (
            data_1m["Low"].iloc[i]
        )

        highest_price = max(
            highest_price,
            high
        )

        trail_stop = max(

            trail_stop,

            highest_price

            -

            (2 * entry_atr)

        )

        stop_hit = (
            low <= trail_stop
        )

        eod_exit = (

            current_time.hour == 15

            and

            current_time.minute >= 15

        )

        if stop_hit or eod_exit:

            exits.iloc[i] = True

            in_trade = False

            entry_atr = None
            highest_price = None
            trail_stop = None

# ==================================================
# PORTFOLIO
# ==================================================

portfolio = vbt.Portfolio.from_signals(

    close=data_1m["Close"],

    entries=entries,

    exits=exits,

    init_cash=100000,

    freq="1m"

)

# ==================================================
# RESULTS
# ==================================================

print()
print("=" * 60)
print("ALPHAFORGE V3 TRAILING STOP")
print("=" * 60)

print()

print(
    "15M Bullish:",
    int(
        context_15m[
            "BULLISH_CONTEXT"
        ].sum()
    )
)

print(
    "5M Setups:",
    int(
        setup_5m.sum()
    )
)

print(
    "1M Triggers:",
    int(
        entries.sum()
    )
)

print(
    "Trades:",
    int(
        portfolio.trades.count()
    )
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

print()

print("=" * 60)
print("TRADES")
print("=" * 60)

trades = portfolio.trades.records_readable

print(trades)

if len(trades) > 0:

    print()

    print(
        "Average Trade Return:",
        round(
            float(
                trades["Return"].mean()
            ),
            4
        )
    )

    print(
        "Best Trade:",
        round(
            float(
                trades["Return"].max()
            ),
            4
        )
    )

    print(
        "Worst Trade:",
        round(
            float(
                trades["Return"].min()
            ),
            4
        )
    )