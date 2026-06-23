import pandas as pd
import yfinance as yf
import vectorbt as vbt

from backtesting.feature_engine import compute_features
from backtesting.mtf_context_engine import build_mtf_context
from backtesting.mtf_broadcast import broadcast_context
from backtesting.mtf_setup_engine import build_5m_setup
from backtesting.mtf_trigger_engine import build_1m_trigger

# ============================================================
# DOWNLOAD DATA
# ============================================================

print("\n" + "=" * 60)
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

for df in [data_15m, data_5m, data_1m]:
    df.columns = df.columns.get_level_values(0)

# ============================================================
# FEATURES
# ============================================================

data_15m = compute_features(data_15m)
data_5m = compute_features(data_5m)
data_1m = compute_features(data_1m)

# ============================================================
# MTF PIPELINE
# ============================================================

context_15m = build_mtf_context(data_15m)

context_5m = broadcast_context(
    context_15m,
    data_5m
)

setup_5m = build_5m_setup(
    data_5m,
    context_5m
)

setup_1m = (
    setup_5m
    .reindex(
        data_1m.index,
        method="ffill"
    )
    .fillna(False)
    .astype(bool)
)

entries = build_1m_trigger(
    data_1m,
    setup_1m
)

# ============================================================
# OPTIMIZATION
# ============================================================

results = []

reward_multiples = [
    2,   # 1:1
    4,   # 1:2
    6,   # 1:3
    8    # 1:4
]

for reward_atr in reward_multiples:

    exits = pd.Series(
        False,
        index=data_1m.index
    )

    in_trade = False

    stop_price = None
    target_price = None

    for i in range(len(data_1m)):

        current_time = (
            data_1m.index[i]
            .tz_convert("Asia/Kolkata")
        )

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
                (2 * atr)
            )

            target_price = (
                entry_price
                +
                (reward_atr * atr)
            )

            in_trade = True

        elif in_trade:

            low = (
                data_1m["Low"].iloc[i]
            )

            high = (
                data_1m["High"].iloc[i]
            )

            stop_hit = (
                low <= stop_price
            )

            target_hit = (
                high >= target_price
            )

            eod_exit = (
                current_time.hour == 15
                and
                current_time.minute >= 15
            )

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

    portfolio = vbt.Portfolio.from_signals(
        close=data_1m["Close"],
        entries=entries,
        exits=exits,
        init_cash=100000,
        freq="1m"
    )

    rr_name = f"1:{reward_atr//2}"

    results.append({

        "RR": rr_name,

        "Trades":
            int(
                portfolio.trades.count()
            ),

        "Return":
            round(
                float(
                    portfolio.total_return()
                ),
                4
            ),

        "Sharpe":
            round(
                float(
                    portfolio.sharpe_ratio()
                ),
                4
            ),

        "WinRate":
            round(
                float(
                    portfolio.trades.win_rate()
                ),
                4
            ),

        "MaxDD":
            round(
                float(
                    portfolio.max_drawdown()
                ),
                4
            )
    })

# ============================================================
# RESULTS
# ============================================================

results_df = pd.DataFrame(results)

print()
print("=" * 80)
print("EXIT OPTIMIZER")
print("=" * 80)
print()

print(results_df)

print()
print("=" * 80)
print("BEST RETURN")
print("=" * 80)
print()

print(
    results_df.loc[
        results_df["Return"].idxmax()
    ]
)

print()
print("=" * 80)
print("BEST SHARPE")
print("=" * 80)
print()

print(
    results_df.loc[
        results_df["Sharpe"].idxmax()
    ]
)