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
# ATR EXITS
# ==================================================

exits = pd.Series(
    False,
    index=data_1m.index
)

in_trade = False

stop_price = None
target_price = None

for i in range(len(data_1m)):

    if entries.iloc[i] and not in_trade:

        entry_price = (
            data_1m["Close"].iloc[i]
        )

        atr = (
            data_1m["ATR14"].iloc[i]
        )

        stop_price = (
            entry_price
            -
            2 * atr
        )

        target_price = (
            entry_price
            +
            6 * atr
        )

        in_trade = True

    elif in_trade:

        low = data_1m["Low"].iloc[i]
        high = data_1m["High"].iloc[i]

        stop_hit = (
            low <= stop_price
        )

        target_hit = (
            high >= target_price
        )

        # =====================================
        # END OF DAY EXIT (3:15 PM IST)
        # =====================================

        current_time = (
            data_1m.index[i]
            .tz_convert("Asia/Kolkata")
        )

        eod_exit = (

            current_time.hour == 15

            and

            current_time.minute >= 15

        )

        # =====================================

        if (
            stop_hit
            or
            target_hit
            or
            eod_exit
        ):

            exits.iloc[i] = True

            in_trade = False

            stop_price = None
            target_price = None

# ==================================================
# BACKTEST
# ==================================================

portfolio = vbt.Portfolio.from_signals(

    close=data_1m["Close"],

    entries=entries,

    exits=exits,

    init_cash=100000,

    freq="1m"

)

# ==================================================
# REPORT
# ==================================================

print()
print("=" * 60)
print("ALPHAFORGE V3 MTF BACKTEST")
print("=" * 60)

print()

print(
    "15M Bullish:",
    int(
        context_15m["BULLISH_CONTEXT"].sum()
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

print()

print(
    portfolio.trades.records_readable.to_string()
)
print()
print("=" * 60)
print("HOLDING TIME ANALYSIS")
print("=" * 60)

trades = portfolio.trades.records_readable

if len(trades) > 0:

    for idx, trade in trades.iterrows():

        duration = (

            trade["Exit Timestamp"]

            -

            trade["Entry Timestamp"]

        )

        print()

        print(
            f"Trade #{idx + 1}"
        )

        print(
            "Entry:",
            trade["Entry Timestamp"]
            .tz_convert("Asia/Kolkata")
        )

        print(
            "Exit:",
            trade["Exit Timestamp"]
            .tz_convert("Asia/Kolkata")
        )

        print(
            "Duration:",
            duration
        )

        print(
            "Return:",
            round(
                trade["Return"],
                4
            )
        )