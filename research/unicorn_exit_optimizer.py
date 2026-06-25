import pandas as pd
import vectorbt as vbt

from backtesting.feature_engine import (
    compute_features
)

print("\n" + "=" * 80)
print("UNICORN EXIT OPTIMIZER")
print("=" * 80)

# ============================================================
# LOAD DATA
# ============================================================

data = pd.read_csv(
    "data/processed/nifty_15m_master.csv"
)

data["datetime"] = pd.to_datetime(
    data["datetime"]
)

data.set_index(
    "datetime",
    inplace=True
)

data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    },
    inplace=True
)

# ============================================================
# FEATURES
# ============================================================

data = compute_features(data)

# ============================================================
# BUILD UNICORN ENTRIES
# ============================================================

entries = pd.Series(
    False,
    index=data.index
)

sweep = data["SWEEP_SWING_LOW"]
mss = data["BOS_BULLISH"]
quality_fvg = data["QUALITY_BULLISH_FVG"]

for i in range(len(data) - 20):

    if not sweep.iloc[i]:
        continue

    mss_window = mss.iloc[
        i:i+6
    ]

    if not mss_window.any():
        continue

    mss_idx = mss_window[
        mss_window
    ].index[0]

    mss_pos = data.index.get_loc(
        mss_idx
    )

    fvg_window = quality_fvg.iloc[
        mss_pos:mss_pos+6
    ]

    if not fvg_window.any():
        continue

    fvg_idx = fvg_window[
        fvg_window
    ].index[0]

    fvg_pos = data.index.get_loc(
        fvg_idx
    )

    fvg_top = data[
        "BullishFVG_Top"
    ].iloc[fvg_pos]

    fvg_bottom = data[
        "BullishFVG_Bottom"
    ].iloc[fvg_pos]

    for j in range(
        fvg_pos + 1,
        min(
            fvg_pos + 11,
            len(data)
        )
    ):

        inside_zone = (

            data["Low"].iloc[j]
            <=
            fvg_top

            and

            data["Low"].iloc[j]
            >=
            fvg_bottom

        )

        bullish_close = (

            data["Close"].iloc[j]
            >
            data["Open"].iloc[j]

        )

        if (
            inside_zone
            and
            bullish_close
        ):

            entries.iloc[j] = True
            break

# ============================================================
# EXIT TESTS
# ============================================================

results = []

for rr in [1, 1.5, 2, 3]:

    exits = pd.Series(
        False,
        index=data.index
    )

    entry_idx = data.index[
        entries
    ]

    for ts in entry_idx:

        pos = data.index.get_loc(ts)

        entry_price = data[
            "Close"
        ].iloc[pos]

        atr = data[
            "ATR14"
        ].iloc[pos]

        stop = (
            entry_price
            -
            atr
        )

        target = (
            entry_price
            +
            (atr * rr)
        )

        for k in range(
            pos + 1,
            len(data)
        ):

            low = data[
                "Low"
            ].iloc[k]

            high = data[
                "High"
            ].iloc[k]

            if low <= stop:

                exits.iloc[k] = True
                break

            if high >= target:

                exits.iloc[k] = True
                break

            # EOD EXIT

            if (

                data.index[k].hour == 9

                and

                data.index[k].minute == 45

            ):

                exits.iloc[k] = True
                break

    portfolio = vbt.Portfolio.from_signals(

        close=data["Close"],

        entries=entries,

        exits=exits,

        init_cash=100000,

        freq="15m"
    )

    results.append({

        "RR": f"1:{rr}",

        "Trades":
            portfolio.trades.count(),

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

        "PF":
            round(
                float(
                    portfolio.trades.profit_factor()
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

results_df = pd.DataFrame(
    results
)

print()

print("=" * 80)
print("UNICORN EXIT OPTIMIZER RESULTS")
print("=" * 80)

print(
    results_df
)

print()

print("=" * 80)
print("BEST PROFIT FACTOR")
print("=" * 80)

print(
    results_df.sort_values(
        "PF",
        ascending=False
    ).head(1)
)

print()

print("=" * 80)
print("BEST RETURN")
print("=" * 80)

print(
    results_df.sort_values(
        "Return",
        ascending=False
    ).head(1)
)